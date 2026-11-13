"""요리 안내. 상태는 코드가 기억, next/prev/repeat 은 LLM 안 부름. (담당: 강준형)"""

from dataclasses import dataclass, field

from core.schema import ToolResult


@dataclass
class CookingState:
    cooking: bool = False
    recipe: str = ""
    steps: list[str] = field(default_factory=list)
    current_step: int = 0


state = CookingState()


def as_context() -> dict | None:
    """프롬프트에 넣을 요리 상태."""
    if not state.cooking:
        return None
    return {"recipe": state.recipe, "current_step": state.current_step + 1, "total": len(state.steps)}


def start_cooking(params: dict) -> ToolResult:
    # TODO(강준형): find_recipe(recipe) 있으면 그 steps, 없으면 params["steps"]
    return ToolResult()


def next_step(params: dict) -> ToolResult:
    # TODO(강준형): 요리 중 아니면 "지금은 요리 중이 아니야"
    return ToolResult()


def prev_step(params: dict) -> ToolResult:
    # TODO(강준형)
    return ToolResult()


def repeat_step(params: dict) -> ToolResult:
    # TODO(강준형)
    return ToolResult()


def stop_cooking(params: dict) -> ToolResult:
    # TODO(강준형)
    return ToolResult()
