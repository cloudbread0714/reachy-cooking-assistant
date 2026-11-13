"""데이터 약속 (노션 ④). 모든 모듈이 이 파일만 보고 주고받아요.

이 파일을 바꾸는 PR은 팀 단톡방에 공유하고 merge해요. (관리: 강유진)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# 감정 목록. 새 감정을 추가하려면 여기 + motion/emotions.py 의 MOVES 둘 다 추가해요.
# ---------------------------------------------------------------------------
EMOTIONS: tuple[str, ...] = (
    "happy",     # 기쁠 때, 칭찬할 때
    "sad",       # 위로할 때, 아쉬울 때
    "curious",   # 궁금할 때, 제안할 때
    "confused",  # 못 알아들었을 때
    "nod",       # 알겠다고 할 때
    "shake",     # 안 된다고 할 때 (유통기한 지난 재료 등)
    "think",     # 생각 중일 때
    "excited",   # 신날 때 (요리 시작)
)
DEFAULT_EMOTION = "nod"

# ---------------------------------------------------------------------------
# action 목록: 이름 -> 꼭 있어야 하는 params
# ---------------------------------------------------------------------------
ACTIONS: dict[str, tuple[str, ...]] = {
    # 재료 관리 (김민석)
    "add_ingredient": ("name",),          # expiry: "YYYY-MM-DD" 또는 None(모르면)
    "remove_ingredient": ("name",),
    "list_ingredients": (),
    "check_expiry": (),
    # 음식 추천 (김민석)
    "recommend_recipe": (),               # query: 선택 ("매운 거")
    # 요리 안내 (강준형)
    "start_cooking": ("recipe",),         # steps: 선택 (레시피 데이터에 없을 때 LLM이 만든 단계)
    "next_step": (),
    "prev_step": (),
    "repeat_step": (),
    "stop_cooking": (),
}

EXPIRY_SOON_DAYS = 3  # check_expiry 에서 "임박" 기준 (고정값)


@dataclass
class Action:
    name: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class Response:
    """LLM 응답 1개."""

    reply: str
    emotion: str = DEFAULT_EMOTION
    action: Action | None = None


@dataclass
class ToolResult:
    """action 실행 결과. 값이 있으면 LLM의 reply/emotion 대신 이걸 써요.

    예: list_ingredients 는 실제 저장된 재료로 말해야 하니까 say 를 채워요.
    """

    say: str | None = None
    emotion: str | None = None


FALLBACK = Response(reply="다시 말해줄래?", emotion="confused", action=None)


def _strip_code_fence(text: str) -> str:
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    return match.group(1) if match else text


def parse_response(raw: str) -> Response:
    """LLM 원문 -> Response. 예외 처리 규칙(노션 ④-6)을 여기서 전부 적용해요."""
    try:
        data = json.loads(_strip_code_fence(raw).strip())
    except (json.JSONDecodeError, TypeError):
        return FALLBACK
    if not isinstance(data, dict):
        return FALLBACK

    reply = data.get("reply")
    if not isinstance(reply, str) or not reply.strip():
        return FALLBACK

    emotion = data.get("emotion")
    if emotion not in EMOTIONS:
        emotion = DEFAULT_EMOTION

    return Response(reply=reply.strip(), emotion=emotion, action=_parse_action(data.get("action")))


def _parse_action(raw: Any) -> Action | None:
    """모르는 action 이나 필수 params 가 빠진 action 은 무시(None)해요."""
    if not isinstance(raw, dict):
        return None
    name = raw.get("name")
    if name not in ACTIONS:
        return None
    params = raw.get("params") or {}
    if not isinstance(params, dict):
        return None
    if any(params.get(key) in (None, "") for key in ACTIONS[name]):
        return None
    return Action(name=name, params=params)
