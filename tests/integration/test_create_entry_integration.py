import pytest
import shutil
from pathlib import Path
from unittest.mock import patch

# Assuming create_entry.py is in the parent directory
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from create_entry import create_new_entry


@pytest.fixture
def temp_content_root(tmp_path: Path) -> Path:
    """Provides a temporary content root directory for testing."""
    test_root = tmp_path / "test_content_root"
    test_root.mkdir()
    yield test_root
    shutil.rmtree(test_root)


@patch(
    "builtins.input",
    side_effect=[
        "test_domain",
        "test_topic",
        "test_subtopic",
        "Test Question for Integration",
        "::END::",
        "Test Answer for Integration",
        "::END::",
        "n",  # No thinking section
        "easy",
        "keyword1, keyword2",
        "",  # Auto-generate filename
    ],
)
@patch("builtins.print")  # Mock print to suppress output during test
def test_create_new_entry_success(mock_print, mock_input, temp_content_root: Path):
    """Test successful creation of a new entry."""
    create_new_entry(content_root=temp_content_root)

    # Verify file creation
    expected_file_path = (
        temp_content_root
        / "test_domain"
        / "test_topic"
        / "test_subtopic"
        / "001_test_question_for_integration.md"
    )
    assert expected_file_path.exists()

    # Verify file content (basic check)
    with open(expected_file_path, "r") as f:
        content = f.read()
        assert "id:" in content
        assert 'domain: "test_domain"' in content
        assert 'topic: "test_topic"' in content
        assert 'subtopic: "test_subtopic"' in content
        assert 'difficulty: "easy"' in content
        assert 'keywords:\n  - "keyword1"\n  - "keyword2"' in content
        assert "# Question\n\nTest Question for Integration" in content
        assert "# Answer\n\nTest Answer for Integration" in content

