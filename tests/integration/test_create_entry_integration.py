import shutil

# Assuming create_entry.py is in the parent directory
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pathlib import Path

from create_entry import create_new_entry


class TestCreateEntryIntegration(unittest.TestCase):
    """Integration tests for the create_entry script."""

    def setUp(self):
        """Set up a temporary content root directory for testing."""
        self.test_content_root = Path("test_content_root")
        if self.test_content_root.exists():
            shutil.rmtree(self.test_content_root)
        self.test_content_root.mkdir()

    def tearDown(self):
        """Clean up the temporary content root directory after testing."""
        if self.test_content_root.exists():
            shutil.rmtree(self.test_content_root)

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
    def test_create_new_entry_success(self, mock_print, mock_input):
        """Test successful creation of a new entry."""
        create_new_entry(content_root=self.test_content_root)

        # Verify file creation
        expected_file_path = (
            self.test_content_root
            / "test_domain"
            / "test_topic"
            / "test_subtopic"
            / "001_test_question_for_integration.md"
        )
        self.assertTrue(expected_file_path.exists())

        # Verify file content (basic check)
        with open(expected_file_path, "r") as f:
            content = f.read()
            self.assertIn("id:", content)
            self.assertIn('domain: "test_domain"', content)
            self.assertIn('topic: "test_topic"', content)
            self.assertIn('subtopic: "test_subtopic"', content)
            self.assertIn('difficulty: "easy"', content)
            self.assertIn('keywords:\n  - "keyword1"\n  - "keyword2"', content)
            self.assertIn("# Question\n\nTest Question for Integration", content)
            self.assertIn("# Answer\n\nTest Answer for Integration", content)


if __name__ == "__main__":
    unittest.main()

