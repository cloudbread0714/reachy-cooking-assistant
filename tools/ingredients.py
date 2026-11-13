"""재료 관리. (담당: 김민석)"""

from core.schema import ToolResult

# TODO(김민석): data/ingredients.json 저장
#   형식: [{"name": "우유", "expiry": "2026-11-20"}, {"name": "두부", "expiry": null}]
#   - 파일 깨졌을 때 빈 목록으로 덮어쓰지 않게 주의


def load() -> list[dict]:
    """main.py 가 프롬프트에 넣으려고 부름."""
    # TODO(김민석)
    return []


def add_ingredient(params: dict) -> ToolResult:
    # TODO(김민석): 같은 이름이면 expiry 만 업데이트, expiry None 이면 "유통기한은 언제까지야?"
    return ToolResult()


def remove_ingredient(params: dict) -> ToolResult:
    # TODO(김민석)
    return ToolResult()


def list_ingredients(params: dict) -> ToolResult:
    # TODO(김민석): 저장된 재료로 say 만들기 (LLM reply 대신 이걸 말함)
    return ToolResult()


def check_expiry(params: dict) -> ToolResult:
    # TODO(김민석): 지남 → "shake", 임박 → "curious". 기준은 core/schema.py EXPIRY_SOON_DAYS
    return ToolResult()
