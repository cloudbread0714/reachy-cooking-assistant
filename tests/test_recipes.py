"""레시피 JSON 형식 검사. 새 레시피 추가하면 자동으로 같이 검사됨."""

import json

import pytest

from core.config import DATA_DIR

FILES = sorted((DATA_DIR / "recipes").glob("*.json"))
REQUIRED = {"name": str, "ingredients": list, "optional": list, "tags": list, "time_min": int, "steps": list}


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_recipe_format(path):
    recipe = json.loads(path.read_text(encoding="utf-8"))
    for key, typ in REQUIRED.items():
        assert isinstance(recipe.get(key), typ), f"{key} 없음/타입 틀림"
    assert recipe["ingredients"] and recipe["steps"]
    assert all(isinstance(s, str) and s.strip() for s in recipe["steps"])
    assert path.stem.isascii(), "파일 이름은 영문"


def test_recipe_names_unique():
    names = [json.loads(p.read_text(encoding="utf-8"))["name"] for p in FILES]
    assert len(names) == len(set(names))
