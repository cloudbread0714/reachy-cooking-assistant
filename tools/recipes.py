"""음식 추천. (담당: 김민석)"""

from core.schema import ToolResult


def recommend_recipe(params: dict) -> ToolResult:
    # TODO(김민석): 가진 재료로 만들 수 있는 레시피 2~3개 추천 (검색은 rag/)
    #   - params["query"] 있으면 반영 ("매운 거")
    #   - 없으면 emotion "sad"
    return ToolResult()
