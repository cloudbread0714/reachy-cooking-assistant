"""요리 안내. (담당: 강준형)"""

from core.schema import ToolResult

# TODO(강준형): 요리 진행 상태 (코드가 기억)
#   {"cooking": bool, "recipe": str, "steps": [...], "current_step": int}


def as_context() -> dict | None:
    """프롬프트에 넣을 요리 상태. 요리 중 아니면 None."""
    # TODO(강준형)
    return None


def start_cooking(params: dict) -> ToolResult:
    # TODO(강준형): 레시피 혼합 방식
    #   1. data/recipes 에 params["recipe"] 있으면 그 steps
    #   2. 없으면 data/generated_recipes/ (전에 LLM 이 만든 것) 에서 찾기
    #   3. 그래도 없으면 LLM 이 만든 params["steps"] 사용 + data/generated_recipes/ 에 저장
    #      (다음에 같은 요리면 같은 순서로 안내, 형식은 data/recipes 와 같게)
    #   4. steps 가 None 이면 (schema 가 이상한 단계 걸러냄) "그 요리 방법을 못 찾았어" + confused
    #   - steps 는 요리 상태에 저장 → next/prev/repeat 은 저장된 리스트만 사용 (LLM 안 부름)
    #   - 첫 단계를 say 로, emotion "excited"
    return ToolResult()


def next_step(params: dict) -> ToolResult:
    # TODO(강준형): current_step + 1 (LLM 안 부름). 요리 중 아니면 "지금은 요리 중이 아니야"
    return ToolResult()


def prev_step(params: dict) -> ToolResult:
    # TODO(강준형): current_step - 1
    return ToolResult()


def repeat_step(params: dict) -> ToolResult:
    # TODO(강준형): 현재 단계 다시 말하기
    return ToolResult()


def stop_cooking(params: dict) -> ToolResult:
    # TODO(강준형): 요리 상태 초기화
    return ToolResult()
