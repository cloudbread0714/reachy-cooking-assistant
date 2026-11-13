import main
from motion.emotions import EmotionPlayer
from tools import ingredients


def test_exit_only_when_whole_sentence():
    assert main.is_exit("종료")
    assert main.is_exit("잘 가!")
    assert not main.is_exit("김치찌개 끓이는 법 잘 가르쳐 줘")


def test_broken_ingredients_file_does_not_end_conversation(tmp_path, monkeypatch, capsys):
    broken = tmp_path / "ingredients.json"
    broken.write_text("[{깨진 json", encoding="utf-8")
    monkeypatch.setattr(ingredients, "PATH", broken)

    main.turn("냉장고에 뭐 있어?", EmotionPlayer(None))

    out = capsys.readouterr().out
    assert "[confused]" in out and "다시 말해줄래" in out
    assert broken.read_text(encoding="utf-8") == "[{깨진 json"  # 깨진 파일을 덮어쓰지 않음
