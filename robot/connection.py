"""Reachy Mini 연결. 연결은 main.py 에서 딱 한 번만 만들어요.

로봇 연결이 필요한 건 motion(감정) 뿐이에요. 음성·카메라는 PC 장치를 직접 써요.
시뮬레이터(데몬)를 먼저 켜야 해요: docs/setup.md 참고
"""

from contextlib import contextmanager
from typing import Iterator


@contextmanager
def connect(use_robot: bool = True) -> Iterator[object | None]:
    """use_robot=False 면 None 을 넘겨줘요. (시뮬레이터 없이 개발할 때)"""
    if not use_robot:
        yield None
        return

    from reachy_mini import ReachyMini

    with ReachyMini() as mini:
        yield mini
