"""텍스트 → 음성. (담당: 강준형)"""


def speak(text: str) -> None:
    """다 말할 때까지 대기."""
    # TODO(강준형): edge-tts (config.TTS_VOICE) → 재생
    print(f"🔊 리치: {text}")
