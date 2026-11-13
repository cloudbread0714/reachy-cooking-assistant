"""음성 → 텍스트. 지금은 키보드 입력 mock. (담당: 강준형)"""


def listen() -> str:
    """한 문장 들을 때까지 대기 후 텍스트 반환."""
    # TODO(강준형): sounddevice 녹음 → Groq Whisper(whisper-large-v3-turbo, language="ko")
    return input("🎤 나: ").strip()
