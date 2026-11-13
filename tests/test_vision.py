import cv2
import numpy as np
import pytest

import main
from core.schema import Action, Response, ToolResult
from tools import dispatcher
from vision import camera
from vision.camera import Camera, encode_jpeg, needs_vision, preprocess, select_sharpest, sharpness
from vision.names import normalize_ingredient


# ---------------------------------------------------------------- 언제 찍을지

@pytest.mark.parametrize("text", [
    "이거 뭐야?", "이게 뭔지 알아?", "내가 손에 들고 있는 거 뭐야", "이거 등록해줘",
    "요거 유통기한 보여?", "사진 보고 알려줘", "이건 어디에 쓰는 거야", "봐봐 이거",
])
def test_needs_vision_true(text):
    assert needs_vision(text)


@pytest.mark.parametrize("text", [
    "냉장고에 뭐 있어?", "우유 등록해줘", "김치찌개 만들래", "다음", "오늘 뭐 먹을까",
    "곧 상하는 거 있어?", "레시피 알려줘",
])
def test_needs_vision_false(text):
    assert not needs_vision(text)


# ---------------------------------------------------------------- 사진 처리

def checkerboard(h=480, w=640, cell=20):
    y, x = np.indices((h, w))
    board = (((y // cell) + (x // cell)) % 2 * 255).astype(np.uint8)
    return cv2.cvtColor(board, cv2.COLOR_GRAY2BGR)


def test_sharpest_frame_is_selected():
    sharp = checkerboard()
    blurry = cv2.GaussianBlur(sharp, (31, 31), 10)
    assert sharpness(sharp) > sharpness(blurry)
    assert select_sharpest([blurry, sharp, blurry]) is sharp
    assert select_sharpest([]) is None


def test_preprocess_crops_center_and_limits_size():
    frame = np.zeros((1080, 1920, 3), np.uint8)
    out = preprocess(frame)
    assert max(out.shape[:2]) == camera.MAX_SIDE
    assert abs(out.shape[1] / out.shape[0] - 1920 / 1080) < 0.01  # 비율 유지

    small = np.zeros((200, 300, 3), np.uint8)
    assert preprocess(small).shape[:2] == (200, 300)  # 작으면 그대로, 확대 안 함


def test_encode_jpeg_is_valid():
    data = encode_jpeg(checkerboard())
    assert data[:2] == b"\xff\xd8"  # JPEG 시작 표시
    assert cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR) is not None


# ---------------------------------------------------------------- 카메라 (가짜)

class FakeCapture:
    def __init__(self, frames, opened=True):
        self.frames, self.opened, self.released = list(frames), opened, False

    def isOpened(self):
        return self.opened

    def read(self):
        if not self.frames:
            return False, None
        return True, self.frames.pop(0)

    def release(self):
        self.released = True


def test_camera_picks_sharpest(monkeypatch):
    monkeypatch.setattr(camera, "WARMUP_SEC", 0)
    monkeypatch.setattr(camera, "BURST_SEC", 0)
    sharp = checkerboard()
    blurry = cv2.GaussianBlur(sharp, (31, 31), 10)
    fake = FakeCapture([blurry, blurry, sharp, blurry])
    cam = Camera(opener=lambda index: fake)
    assert cam.capture() is not None
    cam.release()
    assert fake.released


def test_camera_missing_returns_none():
    cam = Camera(opener=lambda index: FakeCapture([], opened=False))
    assert cam.capture() is None


# ---------------------------------------------------------------- 재료 이름 통일

@pytest.mark.parametrize("raw, expected", [
    ("대파", "대파"), ("대파 한 단", "대파"), ("달걀", "계란"), ("계란 10개", "계란"),
    ("삼겹살 300g", "돼지고기"), ("국산 대파", "대파"), ("두부 한 모", "두부"),
    ("스파게티면", "파스타면"), ("체다치즈", "치즈"), ("참치", "참치캔"),
    ("드래곤프루트", "드래곤프루트"),  # 모르는 재료는 그대로
])
def test_normalize_ingredient(raw, expected):
    assert normalize_ingredient(raw) == expected


def test_dispatch_normalizes_ingredient_name(monkeypatch):
    seen = {}
    monkeypatch.setitem(dispatcher.HANDLERS, "add_ingredient", lambda p: seen.update(p) or ToolResult())
    dispatcher.dispatch(Action("add_ingredient", {"name": "대파 한 단", "expiry": None}))
    assert seen == {"name": "대파", "expiry": None}


# ---------------------------------------------------------------- main 연결

def test_no_camera_does_not_call_llm(monkeypatch):
    monkeypatch.setattr(main, "capture_best_frame", lambda: None)
    monkeypatch.setattr(main.llm, "ask", lambda *a: pytest.fail("카메라 없으면 LLM 부르면 안 됨"))
    assert main.respond("이거 뭐야?") == main.NO_CAMERA


def test_image_is_sent_to_llm(monkeypatch):
    sent = {}
    monkeypatch.setattr(main, "capture_best_frame", lambda: b"jpeg")

    def fake_ask(text, context, image):
        sent["image"] = image
        return Response(reply="대파네!", emotion="happy")

    monkeypatch.setattr(main.llm, "ask", fake_ask)
    assert main.respond("이거 뭐야?") == ("happy", "대파네!")
    assert sent["image"] == b"jpeg"


def test_text_only_does_not_capture(monkeypatch):
    monkeypatch.setattr(main, "capture_best_frame", lambda: pytest.fail("사진 찍으면 안 됨"))
    emotion, say = main.respond("냉장고에 뭐 있어?")
    assert say


def test_recipes_use_standard_names():
    """레시피 데이터에 별칭("참치", "달걀" 등)이 쓰이면 이름 통일이 꼬임 → 표준 이름으로."""
    from vision.names import ALIASES, known_names

    known_names.cache_clear()
    wrong = sorted(set(ALIASES) & known_names())
    assert not wrong, f"레시피에 별칭 대신 표준 이름 써줘: {[(w, ALIASES[w]) for w in wrong]}"


def test_eval_judge():
    from vision.eval import judge

    assert judge("계란", Response(reply="달걀이야!")) == "correct"  # 별칭도 정답
    assert judge("대파", Response(reply="이건 양파야!")) == "wrong"
    assert judge("대파", Response(reply="잘 안 보여", emotion="confused")) == "unsure"
    assert judge("대파", Response(reply="등록할게", action=Action("add_ingredient", {"name": "대파 한 단"}))) == "correct"
