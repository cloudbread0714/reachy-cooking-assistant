"""재료 관리. (담당: 김민석)

data/ingredients.json: [{"name": "우유", "expiry": "2026-11-20"}, {"name": "두부", "expiry": null}]
- 같은 이름 add → expiry 만 업데이트
- expiry None → 저장 후 "유통기한은 언제까지야?"
- 임박 기준: schema.EXPIRY_SOON_DAYS
"""

import json

from core.config import DATA_DIR
from core.schema import ToolResult

PATH = DATA_DIR / "ingredients.json"


def load() -> list[dict]:
    """파일 깨졌으면 예외 그대로 (빈 목록 반환하면 save 가 덮어씀)."""
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
    # TODO(김민석): 저장된 재료로 say 만들기
    return ToolResult()


def check_expiry(params: dict) -> ToolResult:
    # TODO(김민석): 지남 → "shake", 임박 → "curious"
    return ToolResult()
