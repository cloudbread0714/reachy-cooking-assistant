"""사진 인식 정확도 측정. 프롬프트·사진 처리 바꿀 때마다 돌려서 비교. (담당: 강유진)

준비: data/vision_samples/<정답 재료명>/*.jpg   (예: data/vision_samples/대파/1.jpg)
실행: uv run python -m vision.eval
      uv run python -m vision.eval --limit 5     # 재료당 5장만 (무료 한도 아끼기)

정답 판정: reply 에 정답 이름이 들어 있거나, add_ingredient 이름이 정답과 같으면 정답
          confused 로 다시 묻는 건 "보류" 로 따로 셈 (틀린 답보다 나음)
"""

from __future__ import annotations

import argparse
import re
import time
import unicodedata
from datetime import date

import cv2
import numpy as np

from core import llm
from core.config import DATA_DIR
from vision.camera import encode_jpeg, preprocess
from vision.names import ALIASES, known_names, normalize_ingredient

SAMPLE_DIR = DATA_DIR / "vision_samples"
QUESTION = "이거 뭐야?"


def load_image(path) -> bytes | None:
    frame = cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)  # 한글 경로 대응
    return None if frame is None else encode_jpeg(preprocess(frame))


def mentioned(reply: str) -> set[str]:
    """대답에 나온 재료 이름 (표준 이름). 단어 단위라 "양배추야" 에서 "배" 는 안 나옴.

    "달걀이야" → 앞부분 "달걀" → 계란. 조사 목록 대신 단어 앞부분(2글자+)을 전부 정규화해서 봄
    """
    found = set()
    for word in re.findall(r"[가-힣]+", reply):
        for end in range(2, len(word) + 1):
            name = normalize_ingredient(word[:end])
            if name in known_names() or name in ALIASES.values():
                found.add(name)
    return found


def judge(label: str, response) -> str:
    """'correct' / 'unsure' / 'wrong'"""
    if response.action and response.action.name == "add_ingredient":
        if normalize_ingredient(str(response.action.params.get("name", ""))) == label:
            return "correct"
    if label in mentioned(response.reply):
        return "correct"
    return "unsure" if response.emotion == "confused" else "wrong"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="재료당 최대 장수 (0 = 전부)")
    parser.add_argument("--delay", type=float, default=4.0, help="요청 사이 대기(초), 무료 한도 대비")
    args = parser.parse_args()

    if not SAMPLE_DIR.exists():
        raise SystemExit(f"{SAMPLE_DIR} 가 없어. data/vision_samples/<재료명>/*.jpg 로 사진 넣어줘")

    context = {"today": date.today().isoformat(), "ingredients": [], "cooking": None}
    counts = {"correct": 0, "unsure": 0, "wrong": 0, "error": 0}
    for label_dir in sorted(p for p in SAMPLE_DIR.iterdir() if p.is_dir()):
        label = unicodedata.normalize("NFC", label_dir.name)  # macOS 한글 폴더명은 자모 분리(NFD)라 비교 실패함
        images = sorted(p for p in label_dir.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"})
        for path in images[: args.limit or None]:
            image = load_image(path)
            if image is None:
                print(f"건너뜀 (못 읽음): {path}")
                continue
            try:
                response = llm.ask(QUESTION, context, image)
            except Exception as error:  # 한 장 실패로 전체 측정 안 멈추게 (503 등)
                counts["error"] += 1
                print(f"[error  ] {label:8} {path.name:20} → {error!r:.80}")
                continue
            result = judge(label, response)
            counts[result] += 1
            print(f"[{result:7}] {label:8} {path.name:20} → {response.reply}")
            time.sleep(args.delay)

    total = counts["correct"] + counts["unsure"] + counts["wrong"]  # 오류는 빼고 계산
    if total == 0:
        raise SystemExit("측정된 사진이 없어")
    print(f"\n정답 {counts['correct']}/{total} ({counts['correct'] / total:.0%})"
          f" | 다시 묻기 {counts['unsure']} | 오답 {counts['wrong']} | 오류(제외) {counts['error']}")


if __name__ == "__main__":
    main()
