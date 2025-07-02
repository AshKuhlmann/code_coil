import sys
import builtins
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import create_entry  # noqa: E402


def test_get_multiline_input_long_and_odd(monkeypatch):
    lines = [
        "weird start !!!",
        """long line with special chars !@#$%^&*()""" + "x" * 500,
        "::END::",
    ]
    iterator = iter(lines)
    monkeypatch.setattr(builtins, "input", lambda *args: next(iterator))
    result = create_entry.get_multiline_input("prompt")
    expected = "\n".join(lines[:-1])
    assert result == expected


def test_create_entry_with_long_inputs(tmp_path, monkeypatch):
    root = tmp_path / "content" / "python"
    root.mkdir(parents=True)

    long_question = "Q" * 50
    long_answer = "A" * 800
    long_thinking = "T" * 700

    inputs = [
        "domain1",  # domain
        "topic1",  # topic
        "subtopic1",  # subtopic
        long_question,
        "::END::",
        long_answer,
        "::END::",
        "y",  # include thinking
        long_thinking,
        "::END::",
        "hard",  # difficulty
        "kw1, kw2",  # keywords
        "",  # filename
    ]

    iterator = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda *args: next(iterator))
    monkeypatch.setattr(create_entry, "CONTENT_ROOT", str(root))

    create_entry.create_new_entry()

    files = list(Path(root).glob("**/*.md"))
    assert len(files) == 1
    text = files[0].read_text()
    assert long_question in text
    assert long_answer in text
    assert long_thinking in text
