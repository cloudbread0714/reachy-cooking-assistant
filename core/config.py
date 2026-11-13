"""환경 변수(.env) 읽기. API 키는 절대 코드에 직접 쓰지 않아요."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

load_dotenv(ROOT / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
TTS_VOICE = os.getenv("TTS_VOICE", "ko-KR-SunHiNeural")
