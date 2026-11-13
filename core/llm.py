"""LLM 호출. 지금은 mock. (담당: 강준형)"""

import json

from core.prompt import build_system_prompt
from core.schema import Response, parse_response


def ask(user_text: str, context: dict, image: bytes | None = None) -> Response:
    """말(+사진 JPEG) → Response. 응답 깨지면 parse_response 가 FALLBACK 반환."""
    _system_prompt = build_system_prompt(context)

    # TODO(강준형): google-genai 로 Gemini 호출
    #   - system_instruction=_system_prompt
    #   - image 있으면 types.Part.from_bytes(data=image, mime_type="image/jpeg")
    #   - response_mime_type="application/json"
    #   - 응답 텍스트 → parse_response(raw)
    raw = _mock_llm(user_text, image)
    return parse_response(raw)


def _mock_llm(user_text: str, image: bytes | None) -> str:
    """키워드로 흉내만 내는 가짜 LLM (다른 모듈 테스트용)."""
    rules = [
        ("냉장고", {"name": "list_ingredients", "params": {}}),
        ("상하는", {"name": "check_expiry", "params": {}}),
        ("뭐 만들", {"name": "recommend_recipe", "params": {}}),
        ("다음", {"name": "next_step", "params": {}}),
        ("이전", {"name": "prev_step", "params": {}}),
        ("다시", {"name": "repeat_step", "params": {}}),
        ("그만", {"name": "stop_cooking", "params": {}}),
    ]
    action = next((a for keyword, a in rules if keyword in user_text), None)
    reply = "(mock) 사진 받았어!" if image else f"(mock) '{user_text}' 들었어!"
    return json.dumps({"reply": reply, "emotion": "nod", "action": action}, ensure_ascii=False)
