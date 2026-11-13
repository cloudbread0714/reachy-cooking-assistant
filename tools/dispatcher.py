"""action 이름 → 함수. 새 action 은 schema.ACTIONS + HANDLERS 둘 다 추가. (관리: 강유진)"""

from typing import Callable

from core.schema import ACTIONS, Action, ToolResult
from tools import cooking, ingredients, recipes
from vision.names import normalize_ingredient

HANDLERS: dict[str, Callable[[dict], ToolResult]] = {
    "add_ingredient": ingredients.add_ingredient,
    "remove_ingredient": ingredients.remove_ingredient,
    "list_ingredients": ingredients.list_ingredients,
    "check_expiry": ingredients.check_expiry,
    "recommend_recipe": recipes.recommend_recipe,
    "start_cooking": cooking.start_cooking,
    "next_step": cooking.next_step,
    "prev_step": cooking.prev_step,
    "repeat_step": cooking.repeat_step,
    "stop_cooking": cooking.stop_cooking,
}

assert set(HANDLERS) == set(ACTIONS), "ACTIONS 와 HANDLERS 불일치"


NAME_ACTIONS = ("add_ingredient", "remove_ingredient")  # 재료 이름 통일 대상


def dispatch(action: Action | None) -> ToolResult:
    """action 없음 → 빈 결과. 실행 오류 → 사과 + confused."""
    if action is None:
        return ToolResult()
    params = action.params
    if action.name in NAME_ACTIONS and isinstance(params.get("name"), str):
        params = {**params, "name": normalize_ingredient(params["name"])}
    try:
        return HANDLERS[action.name](params)
    except Exception as error:  # 한 기능 오류로 전체 안 멈추게
        print(f"⚠️ {action.name} 실행 오류: {error}")
        return ToolResult(say="미안, 그건 지금 처리하지 못했어.", emotion="confused")
