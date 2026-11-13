"""감정 → 로봇 동작. (담당: 김민석)"""


class EmotionPlayer:
    """main.py 가 쓰는 약속: EmotionPlayer(mini).play(emotion), .wait()"""

    def __init__(self, mini: object | None):
        self.mini = mini  # None 이면 시뮬레이터 없이 실행 중

    def play(self, emotion: str) -> None:
        """바로 리턴해야 함 (말하는 동안 같이 움직이게)."""
        # TODO(김민석): core/schema.py EMOTIONS 8개 동작 구현
        #   - SDK: mini.goto_target(head=create_head_pose(roll=, pitch=, yaw=, degrees=True),
        #                           antennas=[왼, 오](라디안), body_yaw=라디안, duration=초)
        #     create_head_pose 는 reachy_mini.utils 에 있음
        #   - 모르는 감정은 nod
        #   - 스레드로 돌려서 바로 리턴
        #   - mini 가 None 이면 출력만
        #   - 확인용 스크립트 motion/demo.py 새로 만들어도 됨
        print(f"[{emotion}]")  # 임시: 출력만

    def wait(self) -> None:
        """동작 끝날 때까지 대기."""
        # TODO(김민석)
