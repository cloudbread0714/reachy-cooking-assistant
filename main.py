"""실행 파일. (통합: 강유진)

    uv run main.py              # 시뮬레이터 연결 (데몬 먼저)
    uv run main.py --no-robot   # 시뮬레이터 없이

흐름: 듣기 → (사진) → LLM → action → 동작 + 말하기
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

EXIT_WORDS = ("종료", "잘 가", "잘가", "끝내자", "그만 끝내자")


def is_exit(user_text: str) -> bool:
    """문장 전체가 종료 명령일 때만 True. ("잘 가르쳐 줘"는 종료 아님)"""
    return user_text.strip(" .!?~") in EXIT_WORDS


def build_context() -> dict:
    return {
        "today": date.today().isoformat(),
        "ingredients": ingredients.load(),
        "cooking": cooking.as_context(),
    }


def turn(user_text: str, motion: EmotionPlayer) -> None:
    try:
        image = capture_best_frame() if needs_vision(user_text) else None
        response = llm.ask(user_text, build_context(), image)
        result = dispatch(response.action)
        emotion, say = result.emotion or response.emotion, result.say or response.reply
    except Exception as error:  # 한 턴 오류로 대화 안 끝나게
        print(f"⚠️ 처리 중 오류: {error!r}")
        emotion, say = "confused", "미안, 문제가 생겼어. 다시 말해줄래?"

    motion.play(emotion)  # 말하면서 움직임
    speak(say)
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
            if is_exit(user_text):
                motion.play("sad")
                speak("다음에 또 보자!")
                motion.wait()
                break
            turn(user_text, motion)


if __name__ == "__main__":
    main()
