import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from code_coil import hello  # noqa: E402


def test_hello() -> None:
    assert hello() == "hello"
