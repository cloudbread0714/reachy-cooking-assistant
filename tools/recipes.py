"""음식 추천. 검색은 rag/search.py, 여기선 말할 문장만. (담당: 김민석)"""

from core.schema import ToolResult


def recommend_recipe(params: dict) -> ToolResult:
    # TODO(김민석): search_recipes 상위 2~3개로 say, 없으면 emotion "sad"
    return ToolResult()
