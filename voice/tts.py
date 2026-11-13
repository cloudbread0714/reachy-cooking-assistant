"""텍스트 → 음성. (담당: 강준형)"""


def speak(text: str) -> None:
    """다 말할 때까지 대기."""
    # TODO(강준형): edge-tts 로 음성 생성 → PC 스피커 재생
    #   - 목소리는 core.config.TTS_VOICE
    print(f"리치: {text}")  # 임시: 출력만
