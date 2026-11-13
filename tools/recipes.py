"""음식 추천. (담당: 김민석)

레시피 데이터: data/recipes/*.json (형식은 docs/data-contract.md)
검색 로직은 rag/search.py 에 두고 여기서는 불러서 말할 문장만 만들어요.
"""

from core.schema import ToolResult


def recommend_recipe(params: dict) -> ToolResult:
    # TODO(김민석): rag.search.search_recipes(...) 결과 상위 2~3개로 say 만들기
    #   - 만들 수 있는 게 없으면 emotion "sad"
    return ToolResult()
