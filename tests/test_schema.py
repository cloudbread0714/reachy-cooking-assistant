import json

from core.schema import FALLBACK, parse_response


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def test_valid_response():
    raw = dump({"reply": "등록했어!", "emotion": "nod",
                "action": {"name": "add_ingredient", "params": {"name": "우유", "expiry": "2026-11-20"}}})
    r = parse_response(raw)
    assert r.reply == "등록했어!" and r.emotion == "nod"
    assert r.action.name == "add_ingredient" and r.action.params["name"] == "우유"


def test_code_fence_is_ok():
    r = parse_response('```json\n{"reply": "안녕", "emotion": "happy", "action": null}\n```')
    assert r.reply == "안녕" and r.action is None


def test_broken_json_is_fallback():
    assert parse_response("안녕 나는 JSON 아님") == FALLBACK


def test_missing_reply_is_fallback():
    assert parse_response(dump({"emotion": "happy"})) == FALLBACK


def test_unknown_emotion_becomes_nod():
    assert parse_response(dump({"reply": "응", "emotion": "angry"})).emotion == "nod"


def test_unknown_action_is_ignored():
    r = parse_response(dump({"reply": "응", "emotion": "nod", "action": {"name": "fly", "params": {}}}))
    assert r.reply == "응" and r.action is None


def test_non_string_action_name_is_ignored():
    for bad_name in ([], {}, 3, None):
        r = parse_response(dump({"reply": "응", "action": {"name": bad_name}}))
        assert r.reply == "응" and r.action is None


def test_missing_required_param_is_ignored():
    r = parse_response(dump({"reply": "응", "emotion": "nod", "action": {"name": "add_ingredient", "params": {}}}))
    assert r.action is None


def test_expiry_null_is_allowed():
    r = parse_response(dump({"reply": "응", "emotion": "nod",
                             "action": {"name": "add_ingredient", "params": {"name": "두부", "expiry": None}}}))
    assert r.action is not None and r.action.params["expiry"] is None


def start(steps):
    return parse_response(dump({"reply": "시작!", "emotion": "excited",
                                "action": {"name": "start_cooking", "params": {"recipe": "감바스", "steps": steps}}}))


def test_llm_steps_are_kept():
    assert start([" 새우 손질해줘. ", "마늘 썰어줘."]).action.params["steps"] == ["새우 손질해줘.", "마늘 썰어줘."]


def test_bad_llm_steps_become_none():
    for bad in ("새우 볶기", [], [""], [1, 2], ["a"] * 21, None):
        r = start(bad)
        assert r.action.name == "start_cooking" and r.action.params["steps"] is None
