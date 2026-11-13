"""action 이름 -> 실행 함수 연결. (관리: 강유진)

새 action 을 추가하면: schema.ACTIONS + 여기 HANDLERS 두 곳에 추가해요.
"""

from typing import Callable

from core.schema import ACTIONS, Action, ToolResult
from tools import cooking, ingredients, recipes

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

assert set(HANDLERS) == set(ACTIONS), "schema.ACTIONS 와 HANDLERS 가 맞지 않아요"


def dispatch(action: Action | None) -> ToolResult:
    """action 이 없거나 실행 중 오류가 나면 빈 ToolResult (= LLM reply 그대로 말하기)."""
    if action is None:
        return ToolResult()
    try:
        return HANDLERS[action.name](action.params)
    except Exception as error:  # 한 기능 오류로 로봇 전체가 멈추지 않게
        print(f"⚠️ {action.name} 실행 오류: {error}")
        return ToolResult(say="미안, 그건 지금 처리하지 못했어.", emotion="confused")
