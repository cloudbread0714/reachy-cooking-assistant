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
    #   - data/recipes 에 params["recipe"] 있으면 그 steps
    #   - 없으면 LLM 이 만든 params["steps"]
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
