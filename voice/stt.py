"""음성 -> 텍스트. (담당: 강준형)

지금은 키보드 입력이 mock 이에요. 그래서 마이크 없이도 main.py 가 돌아가요.
"""


def listen() -> str:
    """사용자가 한 문장 말할 때까지 기다렸다가 텍스트로 돌려줘요. (blocking)"""
    # TODO(강준형): sounddevice 로 PC 마이크 녹음 -> Groq Whisper(whisper-large-v3-turbo, language="ko")
    return input("🎤 나: ").strip()
