"""Basic tests for the code_coil package.
"""

"""Basic tests for the code_coil package."""
import pytest

from code_coil import hello


def test_hello() -> None:
    """Test the hello function."""
    assert hello() == "hello"
