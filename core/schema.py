"""데이터 약속 (노션 ④). 모든 모듈이 이 파일 기준. 바꾸면 단톡방 공유. (관리: 강유진)"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

# 감정 추가 시 motion/emotions.py 에도 동작 추가
EMOTIONS: tuple[str, ...] = (
    "happy",     # 기쁨, 칭찬, 인사
    "sad",       # 위로, 아쉬움
    "curious",   # 궁금, 제안
    "confused",  # 못 알아들음
    "nod",       # 알겠어
    "shake",     # 안 돼 (유통기한 지남 등)
    "think",     # 생각 중
    "excited",   # 신남 (요리 시작)
)
DEFAULT_EMOTION = "nod"

# action 이름 → 필수 params
ACTIONS: dict[str, tuple[str, ...]] = {
    # 재료 관리 (김민석)
    "add_ingredient": ("name",),          # expiry: "YYYY-MM-DD" 또는 None
    "remove_ingredient": ("name",),
    "list_ingredients": (),
    "check_expiry": (),
    # 음식 추천 (김민석)
    "recommend_recipe": (),               # query: 선택 ("매운 거")
    # 요리 안내 (강준형)
    "start_cooking": ("recipe",),         # steps: 선택 (레시피 데이터에 없을 때)
    "next_step": (),
    "prev_step": (),
    "repeat_step": (),
    "stop_cooking": (),
}

EXPIRY_SOON_DAYS = 3  # 임박 기준 (임시, 2차 회의에서 결정)


@dataclass
class Action:
    name: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class Response:
    """LLM 응답."""

    reply: str
    emotion: str = DEFAULT_EMOTION
    action: Action | None = None


@dataclass
class ToolResult:
    """action 결과. 값 있으면 LLM reply/emotion 대신 사용. (예: 재료 목록은 코드가 직접 말함)"""

    say: str | None = None
    emotion: str | None = None


FALLBACK = Response(reply="다시 말해줄래?", emotion="confused", action=None)


def _strip_code_fence(text: str) -> str:
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    return match.group(1) if match else text


def parse_response(raw: str) -> Response:
    """LLM 원문 → Response. 예외 처리 규칙(노션 ④-6) 전부 여기서."""
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
    """모르는 action, 필수 params 없는 action → None (무시)."""
    if not isinstance(raw, dict):
        return None
    name = raw.get("name")
    if not isinstance(name, str) or name not in ACTIONS:
        return None
    params = raw.get("params") or {}
    if not isinstance(params, dict):
        return None
    if any(params.get(key) in (None, "") for key in ACTIONS[name]):
        return None
    return Action(name=name, params=params)
