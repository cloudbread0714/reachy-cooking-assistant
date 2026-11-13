import main
from motion.emotions import EmotionPlayer
from tools import ingredients


def test_exit_only_when_whole_sentence():
    assert main.is_exit("종료")
    assert main.is_exit("잘 가!")
    assert not main.is_exit("김치찌개 끓이는 법 잘 가르쳐 줘")


def test_error_in_turn_does_not_end_conversation(monkeypatch, capsys):
    def broken_load():
        raise ValueError("ingredients.json 깨짐")

    monkeypatch.setattr(ingredients, "load", broken_load)
    main.turn("냉장고에 뭐 있어?", EmotionPlayer(None))

    out = capsys.readouterr().out
    assert "[confused]" in out and "다시 말해줄래" in out
