from core.schema import ACTIONS, Action, ToolResult
from tools.dispatcher import HANDLERS, dispatch


def test_every_action_has_handler():
    assert set(HANDLERS) == set(ACTIONS)


def test_no_action_returns_empty_result():
    assert dispatch(None) == ToolResult()


def test_handler_error_does_not_crash(monkeypatch):
    def boom(params):
        raise RuntimeError("boom")

    monkeypatch.setitem(HANDLERS, "list_ingredients", boom)
    result = dispatch(Action(name="list_ingredients"))
    assert result.emotion == "confused"
