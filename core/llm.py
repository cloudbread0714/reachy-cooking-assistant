"""LLM 호출. (담당: 강준형)"""

from core.schema import Response


def ask(user_text: str, context: dict, image: bytes | None = None) -> Response:
    """말(+사진 JPEG) → Response."""
    # TODO(강준형): Gemini 호출
    #   - system_instruction = core.prompt.build_system_prompt(context)
    #   - image 있으면 같이 보내기 (mime_type="image/jpeg")
    #   - JSON 응답 강제 (response_mime_type="application/json")
    #   - 응답 텍스트 → core.schema.parse_response(raw) 로 변환해서 반환
    #   - 키·모델명은 core.config (GEMINI_API_KEY, GEMINI_MODEL)
    return Response(reply=f"(mock) {user_text}")  # 임시: 다른 모듈 테스트용
