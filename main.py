"""요리 도우미 로봇 실행 파일. (통합: 강유진)

    uv run main.py              # 시뮬레이터 연결 (데몬 먼저 실행)
    uv run main.py --no-robot   # 시뮬레이터 없이 (모션은 글자로 출력)

흐름: 듣기 -> (필요하면 사진) -> LLM -> action 실행 -> 감정 동작 + 말하기
"""

import argparse
from datetime import date

from core import llm
from robot.connection import connect
from motion.emotions import EmotionPlayer
from tools import cooking, ingredients
from tools.dispatcher import dispatch
from vision.camera import capture_best_frame, needs_vision
from voice.stt import listen
from voice.tts import speak

EXIT_WORDS = ("종료", "잘 가", "끝내자")


def build_context() -> dict:
    return {
        "today": date.today().isoformat(),
        "ingredients": ingredients.load(),
        "cooking": cooking.as_context(),
    }


def turn(user_text: str, motion: EmotionPlayer) -> None:
    image = capture_best_frame() if needs_vision(user_text) else None
    response = llm.ask(user_text, build_context(), image)
    result = dispatch(response.action)

    motion.play(result.emotion or response.emotion)  # 말하는 동안 같이 움직임
    speak(result.say or response.reply)
    motion.wait()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-robot", action="store_true", help="시뮬레이터 없이 실행")
    args = parser.parse_args()

    with connect(use_robot=not args.no_robot) as mini:
        motion = EmotionPlayer(mini)
        motion.play("happy")
        speak("안녕! 오늘은 뭐 만들어볼까?")
        motion.wait()

        while True:
            try:
                user_text = listen()
            except (KeyboardInterrupt, EOFError):
                break
            if not user_text:
                continue
            if any(word in user_text for word in EXIT_WORDS):
                motion.play("sad")
                speak("다음에 또 보자!")
                motion.wait()
                break
            turn(user_text, motion)


if __name__ == "__main__":
    main()
