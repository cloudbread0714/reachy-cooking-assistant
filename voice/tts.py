"""텍스트 -> 음성. (담당: 강준형)"""


def speak(text: str) -> None:
    """text 를 PC 스피커로 말해요. 다 말할 때까지 기다려요. (blocking)"""
    # TODO(강준형): edge-tts (config.TTS_VOICE) 로 mp3 생성 -> 재생
    print(f"🔊 리치: {text}")
