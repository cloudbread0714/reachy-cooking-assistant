"""Reachy Mini 연결. main.py 에서 한 번만 연결하고 motion 에만 넘김."""

from contextlib import contextmanager
from typing import Iterator


@contextmanager
def connect(use_robot: bool = True) -> Iterator[object | None]:
    """use_robot=False 면 None (시뮬레이터 없이 개발)."""
    if not use_robot:
        yield None
        return

    from reachy_mini import ReachyMini

    # 카메라·마이크는 PC 장치 직접 사용 → 로봇 미디어 끔
    with ReachyMini(media_backend="no_media") as mini:
        yield mini
