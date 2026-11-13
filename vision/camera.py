"""웹캠 → LLM 에 보낼 사진. 인식은 LLM 이 하고, 여기선 언제 찍을지 + 사진 품질. (담당: 강유진)

흐름: 여러 장 찍기 → 가장 선명한 한 장 → 가운데 crop + 축소 → JPEG
"""

from __future__ import annotations

import atexit
import os
import re
import time
from typing import Callable

import cv2
import numpy as np

from core.config import DATA_DIR

CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", "0"))
CAPTURE_SIZE = (1280, 720)  # 요청 해상도
WARMUP_SEC = 0.3      # 켜자마자 나오는 어두운 프레임 버림
BURST_SEC = 0.5       # 이 시간 동안 찍은 것 중 가장 선명한 것 선택
CROP_RATIO = 0.8      # 가운데 80% 만 (손에 든 물건이 보통 가운데)
MAX_SIDE = 768        # 긴 변 최대 크기 (토큰·속도 절약)
JPEG_QUALITY = 85
MIN_SHARPNESS = 15.0  # 이보다 흐리면 "흐림" 판정
LAST_CAPTURE = DATA_DIR / "last_capture.jpg"  # 디버그용, 커밋 안 함

# 지시어나 "보여주는" 표현이 있을 때만 사진. "우유 등록해줘" 같은 말로만 하는 등록은 사진 없음
_VISION_PATTERN = re.compile(
    r"(이거|이게|이건|이것|요거|요게|요건|저거|저게|저건)"
    r"|(들고 ?있|손에|보여 ?줄게|보이(니|지|냐|나)|봐 ?봐|봐 ?줘|사진)"
)


def needs_vision(user_text: str) -> bool:
    """사진 필요한 말인지. 필요할 때만 찍어서 무료 API 요청 아낌."""
    return bool(_VISION_PATTERN.search(user_text))


# ---------------------------------------------------------------- 사진 처리 (순수 함수, 테스트 대상)

def sharpness(frame: np.ndarray) -> float:
    """선명도 = Laplacian 분산. 흔들리거나 초점 안 맞으면 작아짐."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if frame.ndim == 3 else frame
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def select_sharpest(frames: list[np.ndarray]) -> np.ndarray | None:
    return max(frames, key=sharpness) if frames else None


def preprocess(frame: np.ndarray) -> np.ndarray:
    """가운데 crop + 긴 변 MAX_SIDE 로 축소."""
    h, w = frame.shape[:2]
    ch, cw = int(h * CROP_RATIO), int(w * CROP_RATIO)
    top, left = (h - ch) // 2, (w - cw) // 2
    frame = frame[top:top + ch, left:left + cw]
    scale = MAX_SIDE / max(ch, cw)
    if scale < 1:
        frame = cv2.resize(frame, (int(cw * scale), int(ch * scale)), interpolation=cv2.INTER_AREA)
    return frame


def encode_jpeg(frame: np.ndarray) -> bytes:
    ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
    if not ok:
        raise ValueError("JPEG 인코딩 실패")
    return buf.tobytes()


# ---------------------------------------------------------------- 카메라

class Camera:
    """한 번 열면 계속 재사용 (열 때마다 1초 가까이 걸려서)."""

    def __init__(self, index: int = CAMERA_INDEX, opener: Callable[[int], object] = cv2.VideoCapture):
        self.index = index
        self._opener = opener
        self._cap = None

    def _ensure_open(self) -> bool:
        if self._cap is not None and self._cap.isOpened():
            return True
        self._cap = self._opener(self.index)
        if not self._cap.isOpened():
            self._cap = None
            return False
        if hasattr(self._cap, "set"):  # 지원하면 HD 로 (안 되면 카메라 기본값 유지)
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_SIZE[0])
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_SIZE[1])
        self._read_for(WARMUP_SEC)
        return True

    def _read_for(self, seconds: float) -> list[np.ndarray]:
        frames, end = [], time.monotonic() + seconds
        while time.monotonic() < end or not frames:
            ok, frame = self._cap.read()
            if not ok:
                break
            frames.append(frame)
        return frames

    def capture(self) -> np.ndarray | None:
        """BURST_SEC 동안 찍은 것 중 가장 선명한 프레임. 카메라 없으면 None."""
        if not self._ensure_open():
            return None
        return select_sharpest(self._read_for(BURST_SEC))

    def release(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None


_camera = Camera()
atexit.register(_camera.release)


def prepare_camera() -> bool:
    """시작할 때 미리 켜둠 (첫 촬영 2초 → 0.5초). 카메라 없으면 False."""
    return _camera._ensure_open()


def capture_best_frame() -> bytes | None:
    """가장 선명한 한 장 JPEG. 카메라 없으면 None."""
    frame = _camera.capture()
    if frame is None:
        return None
    frame = preprocess(frame)
    if sharpness(frame) < MIN_SHARPNESS:
        print(f"⚠️ 사진이 흐려요 (선명도 {sharpness(frame):.1f})")
    data = encode_jpeg(frame)
    try:
        LAST_CAPTURE.parent.mkdir(parents=True, exist_ok=True)
        LAST_CAPTURE.write_bytes(data)
    except OSError:
        pass
    return data
