"""재료 이름 통일. 말·사진 어느 쪽으로 등록해도 레시피 데이터와 같은 이름으로. (담당: 강유진)

"대파 한 단" → "대파", "달걀" → "계란", "삼겹살" → "돼지고기"
"""

from __future__ import annotations

import json
import re
from functools import lru_cache

from core.config import DATA_DIR

# 다른 이름 → 레시피 데이터 이름
ALIASES: dict[str, str] = {
    "달걀": "계란", "계란후라이": "계란",
    "파": "대파", "쪽파": "대파",
    "삼겹살": "돼지고기", "목살": "돼지고기", "앞다리살": "돼지고기", "대패삼겹살": "돼지고기", "돼지": "돼지고기",
    "소": "소고기", "쇠고기": "소고기", "한우": "소고기", "우삼겹": "소고기", "불고기용": "소고기",
    "닭": "닭고기", "닭다리": "닭고기", "닭다리살": "닭고기",
    "스파게티": "파스타면", "스파게티면": "파스타면", "파스타": "파스타면", "펜네": "파스타면",
    "국수": "소면",
    "체다치즈": "치즈", "슬라이스치즈": "치즈", "모짜렐라": "치즈", "모짜렐라치즈": "치즈",
    "양송이": "버섯", "새송이": "버섯", "표고": "버섯", "팽이버섯": "버섯", "느타리": "버섯",
    "소세지": "소시지", "비엔나": "소시지", "비엔나소시지": "소시지",
    "런천미트": "스팸",
    "참치": "참치캔",
    "토마토케첩": "케첩",
    "식빵한봉지": "식빵",
}

# 수량·단위 표현 제거 ("한 단", "200g", "반 개", "두 모")
_AMOUNT = re.compile(
    r"\s*(\d+(\.\d+)?|한|두|세|네|다섯|반)\s*"
    r"(개|단|모|팩|봉지|봉|통|캔|병|줌|장|알|쪽|근|g|kg|ml|l|컵|큰술|작은술|덩이|마리)\b",
    re.IGNORECASE,
)


@lru_cache(maxsize=1)
def known_names() -> frozenset[str]:
    """레시피 데이터에 나오는 재료 이름 전부."""
    names: set[str] = set()
    for path in (DATA_DIR / "recipes").glob("*.json"):
        recipe = json.loads(path.read_text(encoding="utf-8"))
        names.update(recipe.get("ingredients", []))
        names.update(recipe.get("optional", []))
    return frozenset(names)


def normalize_ingredient(name: str) -> str:
    """레시피 데이터 기준 이름으로. 모르는 재료면 정리만 해서 그대로."""
    cleaned = _AMOUNT.sub("", name).strip()
    compact = cleaned.replace(" ", "")
    if not compact:
        return name.strip()

    known = known_names()
    if compact in known:
        return compact
    if compact in ALIASES:
        return ALIASES[compact]

    # "국산 대파", "냉동 새우" → 아는 이름이 끝에 붙어 있으면 그걸로 (가장 긴 것 우선)
    for candidate in sorted({*known, *ALIASES}, key=len, reverse=True):
        if len(candidate) >= 2 and compact.endswith(candidate):
            return ALIASES.get(candidate, candidate)
    return compact
