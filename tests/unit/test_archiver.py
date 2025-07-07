# tests/unit/test_archiver.py

import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from zenith_archive.archiver import Archiver

class TestArchiver(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock()
        self.rules = {"DOCS": [".txt"], "PICS": [".jpg"]}
        self.ignore = ["ignore.me"]
        self.docs_dir = Path("/tmp/sorted")

        self.archiver = Archiver(
            rules=self.rules,
            ignore_list=self.ignore,
            documents_dir=self.docs_dir,
            logger=self.mock_logger,
        )

    def test_invert_rules(self):
        inverted = self.archiver._invert_rules(self.rules)
        self.assertEqual(inverted, {".txt": "DOCS", ".jpg": "PICS"})

    @patch("shutil.move")
    @patch("pathlib.Path.mkdir")
    def test_sort_file(self, mock_mkdir, mock_move):
        test_file = Path("/tmp/source/test.txt")
        self.archiver._sort_file(test_file)

        expected_dest_dir = self.docs_dir / "DOCS"
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_move.assert_called_once_with(str(test_file), str(expected_dest_dir / "test.txt"))
        self.mock_logger.info.assert_called()

    def test_sort_file_no_rule(self):
        test_file = Path("/tmp/source/test.unknown")
        self.archiver._sort_file(test_file)
        self.mock_logger.info.assert_called_with(
            "No rule found for extension '.unknown', skipping: test.unknown"
        )

    def test_sort_directory_nonexistent(self):
        self.archiver.sort_directory(Path("/nonexistent/dir"))
        self.mock_logger.error.assert_called()

if __name__ == "__main__":
    unittest.main()