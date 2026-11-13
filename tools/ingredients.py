"""재료 관리. (담당: 김민석)

저장 형식 (data/ingredients.json):
    [{"name": "우유", "expiry": "2026-11-20"}, {"name": "두부", "expiry": null}]

규칙 (노션 ④-3):
- 같은 이름으로 add 하면 새로 추가하지 않고 expiry 만 업데이트
- expiry 가 None 이면 저장 후 "유통기한은 언제까지야?" 라고 묻기
- 날짜 계산은 코드가 해요. 임박 기준은 schema.EXPIRY_SOON_DAYS (3일)
"""

import json

from core.config import DATA_DIR
from core.schema import ToolResult

PATH = DATA_DIR / "ingredients.json"


def load() -> list[dict]:
    if not PATH.exists():
        return []
    return json.loads(PATH.read_text(encoding="utf-8"))


def save(items: list[dict]) -> None:
    PATH.parent.mkdir(parents=True, exist_ok=True)
    PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def add_ingredient(params: dict) -> ToolResult:
    # TODO(김민석)
    return ToolResult()


def remove_ingredient(params: dict) -> ToolResult:
    # TODO(김민석)
    return ToolResult()


def list_ingredients(params: dict) -> ToolResult:
    # TODO(김민석): 실제 저장된 재료로 say 만들기 (LLM reply 대신 이걸 말해요)
    return ToolResult()


def check_expiry(params: dict) -> ToolResult:
    # TODO(김민석): 지난 재료 -> emotion "shake", 3일 이내 -> "curious"
    return ToolResult()
