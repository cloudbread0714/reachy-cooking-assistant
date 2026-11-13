"""감정 -> 로봇 동작. (담당: 김민석)

MOVES 의 키프레임만 고치면 동작이 바뀌어요. 아래 값은 출발점이에요.
시뮬레이터로 보면서 각도/시간을 다듬어 주세요.

SDK (reachy-mini 1.14):
    mini.goto_target(head=create_head_pose(roll=, pitch=, yaw=, degrees=True),
                     antennas=[왼쪽, 오른쪽](라디안), body_yaw=라디안, duration=초)
"""

from __future__ import annotations

import math
import threading

from core.schema import DEFAULT_EMOTION, EMOTIONS

# 키프레임: (head 각도 dict(도), antennas [라디안, 라디안], body_yaw 도, duration 초)
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

assert set(MOVES) >= set(EMOTIONS), "schema.EMOTIONS 의 감정은 MOVES 에 모두 있어야 해요"


class EmotionPlayer:
    """play() 는 바로 돌아와요(non-blocking). 그래서 말하는 동안 같이 움직여요."""

    def __init__(self, mini: object | None):
        self.mini = mini  # None 이면 출력만 해요 (시뮬레이터 없이 개발)
        self._thread: threading.Thread | None = None

    def play(self, emotion: str) -> None:
        if emotion not in MOVES:
            emotion = DEFAULT_EMOTION
        if self.mini is None:
            print(f"🤖 [{emotion}]")
            return
        if self._thread and self._thread.is_alive():
            self._thread.join()  # 이전 동작이 끝나고 시작
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
