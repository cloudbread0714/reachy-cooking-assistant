"""레시피 검색 (RAG 의 Retrieval 부분). (담당: 김민석)

1단계: 가진 재료와 레시피 재료가 얼마나 겹치는지로 점수 (임베딩 없이도 동작)
2단계: query("매운 거") 가 있으면 임베딩 유사도를 더해서 순위 조정
"""

import json

from core.config import DATA_DIR

RECIPE_DIR = DATA_DIR / "recipes"


def load_recipes() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(RECIPE_DIR.glob("*.json"))]


def find_recipe(name: str) -> dict | None:
    """요리 이름으로 레시피 하나 찾기. (start_cooking 에서 사용)"""
    return next((r for r in load_recipes() if r["name"] == name), None)


def search_recipes(ingredient_names: list[str], query: str | None = None, k: int = 3) -> list[dict]:
    """가진 재료로 만들 수 있는 레시피 상위 k개."""
    # TODO(김민석): 재료 겹침 점수 + (선택) query 임베딩 유사도
    return []
