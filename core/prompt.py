"""시스템 프롬프트. (담당: 강준형)"""


def build_system_prompt(context: dict) -> str:
    """context: {"today": "YYYY-MM-DD", "ingredients": [...], "cooking": {...} | None}"""
    # TODO(강준형): 프롬프트 작성
    #   - 응답은 {"reply", "emotion", "action"} JSON 만 (docs/data-contract.md)
    #   - emotion / action 목록은 core/schema.py 의 EMOTIONS, ACTIONS 에서 가져와서 넣기
    #   - 오늘 날짜 넣기 ("20일까지" → expiry YYYY-MM-DD 변환용)
    #   - 유통기한 모르면 expiry null
    #   - 사진 오면 사진 보고 대답, 애매하면 confused + 다시 보여달라고 (사진 규칙은 강유진과 협의)
    #   - 요리 데이터에 없는 요리면 start_cooking params.steps 에 단계 생성 (한 단계 한 동작, 반말)
    #   - 재료 목록·날짜 계산·단계 이동은 코드가 하니까 지어내지 말라고
    #   - context 의 재료 목록, 요리 상태 넣기
    return ""
