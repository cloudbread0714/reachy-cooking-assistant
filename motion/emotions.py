"""감정 → 로봇 동작. MOVES 키프레임만 고치면 됨. (담당: 김민석)

goto_target(head=create_head_pose(roll, pitch, yaw, degrees=True),
            antennas=[왼, 오](라디안), body_yaw=라디안, duration=초)
확인: uv run python -m motion.demo
"""

from __future__ import annotations

import math
import threading

from core.schema import DEFAULT_EMOTION, EMOTIONS

# (head 각도(도), antennas(라디안), body_yaw(도), duration(초))
Frame = tuple[dict, list[float], float, float]

NEUTRAL: Frame = ({}, [0.0, 0.0], 0, 0.4)

MOVES: dict[str, list[Frame]] = {
    "happy": [({"pitch": -10}, [0.6, -0.6], 0, 0.3), ({}, [-0.6, 0.6], 0, 0.3), ({}, [0.6, -0.6], 0, 0.3)],
    "sad": [({"pitch": 20}, [-1.0, 1.0], 0, 1.0)],
    "curious": [({"roll": 20}, [0.3, 0.3], 0, 0.6)],
    "confused": [({"roll": -20}, [0.8, -0.2], 0, 0.5), ({"roll": 20}, [-0.2, 0.8], 0, 0.5)],
    "nod": [({"pitch": 15}, [0.0, 0.0], 0, 0.3), ({"pitch": -5}, [0.0, 0.0], 0, 0.3)],
    "shake": [({"yaw": 20}, [0.0, 0.0], 0, 0.25), ({"yaw": -20}, [0.0, 0.0], 0, 0.25), ({"yaw": 20}, [0.0, 0.0], 0, 0.25)],
    "think": [({"pitch": -10, "yaw": 15}, [0.4, 0.0], 0, 0.8)],
    "excited": [({"pitch": -15}, [0.8, -0.8], 20, 0.3), ({"pitch": -15}, [-0.8, 0.8], -20, 0.3)],
}

assert set(MOVES) >= set(EMOTIONS), "EMOTIONS 의 감정이 MOVES 에 다 있어야 함"


class EmotionPlayer:
    """play() 는 바로 리턴 → 말하면서 움직임."""

    def __init__(self, mini: object | None):
        self.mini = mini  # None 이면 출력만
        self._thread: threading.Thread | None = None

    def play(self, emotion: str) -> None:
        if emotion not in MOVES:
            emotion = DEFAULT_EMOTION
        if self.mini is None:
            print(f"🤖 [{emotion}]")
            return
        if self._thread and self._thread.is_alive():
            self._thread.join()  # 이전 동작 끝나고 시작
        self._thread = threading.Thread(target=self._run, args=(MOVES[emotion],), daemon=True)
        self._thread.start()

    def wait(self) -> None:
        if self._thread:
            self._thread.join()

    def _run(self, frames: list[Frame]) -> None:
        from reachy_mini.utils import create_head_pose

        for head, antennas, body_yaw, duration in [*frames, NEUTRAL]:
            self.mini.goto_target(
                head=create_head_pose(**head, degrees=True),
                antennas=antennas,
                body_yaw=math.radians(body_yaw),
                duration=duration,
            )
