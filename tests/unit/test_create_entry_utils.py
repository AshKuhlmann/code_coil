import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import os
import shutil

# Assuming create_entry.py is in the parent directory
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from create_entry import get_existing_dirs, sanitize_filename, select_from_list, get_multiline_input, INPUT_TERMINATOR

class TestCreateEntryUtils(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path("test_temp_dir")
        self.test_dir.mkdir(exist_ok=True)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_get_existing_dirs(self):
        (self.test_dir / "dir1").mkdir()
        (self.test_dir / "dir2").mkdir()
        (self.test_dir / "file.txt").touch()
        self.assertEqual(get_existing_dirs(self.test_dir), ["dir1", "dir2"])

        # Test with non-existent path
        self.assertEqual(get_existing_dirs(Path("non_existent_dir")), [])

        # Test with empty directory
        self.assertEqual(get_existing_dirs(self.test_dir), ["dir1", "dir2"])

    def test_sanitize_filename(self):
        self.assertEqual(sanitize_filename("Hello World!"), "hello_world")
        self.assertEqual(sanitize_filename("  Another File Name  "), "another_file_name")
        self.assertEqual(sanitize_filename("File with.dots-and_underscores"), "file_with.dots-and_underscores")
        self.assertEqual(sanitize_filename("File with special chars:<>/|?*"), "file_with_special_chars")
        self.assertEqual(sanitize_filename("A" * 100), "a" * 60) # Test truncation

    @patch('builtins.input', side_effect=['new_item'])
    def test_select_from_list_new_item(self, mock_input):
        options = ["item1", "item2"]
        self.assertEqual(select_from_list(options, "test_prompt"), "new_item")

    @patch('builtins.input', side_effect=['1'])
    def test_select_from_list_existing_item_by_number(self, mock_input):
        options = ["item1", "item2"]
        self.assertEqual(select_from_list(options, "test_prompt"), "item1")

    @patch('builtins.input', side_effect=['Item2'])
    def test_select_from_list_existing_item_by_name(self, mock_input):
        options = ["item1", "item2"]
        self.assertEqual(select_from_list(options, "test_prompt"), "item2")

    @patch('builtins.input', side_effect=['line1', 'line2', INPUT_TERMINATOR])
    def test_get_multiline_input(self, mock_input):
        self.assertEqual(get_multiline_input("Test Prompt"), "line1\nline2")

    @patch('builtins.input', side_effect=[INPUT_TERMINATOR])
    def test_get_multiline_input_empty(self, mock_input):
        self.assertEqual(get_multiline_input("Test Prompt"), "")

if __name__ == '__main__':
    unittest.main()
