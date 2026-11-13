"""감정 8개를 차례로 재생해서 시뮬레이터에서 눈으로 확인하는 스크립트. (담당: 김민석)

    uv run python -m motion.demo            # 전부
    uv run python -m motion.demo nod shake  # 골라서
"""

import sys

from motion.emotions import MOVES, EmotionPlayer
from robot.connection import connect


def main() -> None:
    emotions = sys.argv[1:] or list(MOVES)
    with connect() as mini:
        player = EmotionPlayer(mini)
        for emotion in emotions:
            print(f"재생: {emotion}")
            player.play(emotion)
            player.wait()


if __name__ == "__main__":
    main()
