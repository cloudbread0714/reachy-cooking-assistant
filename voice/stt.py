"""음성 → 텍스트. (담당: 강준형)"""


def listen() -> str:
    """한 문장 들을 때까지 대기 후 텍스트 반환."""
    # TODO(강준형): PC 마이크 녹음 → Groq Whisper(whisper-large-v3-turbo, language="ko")
    #   - 말 끝나면(무음) 자동 종료되게 (voice/recorder.py 새로 만들어도 됨)
    #   - 키는 core.config.GROQ_API_KEY
    return input("나: ").strip()  # 임시: 키보드 입력
