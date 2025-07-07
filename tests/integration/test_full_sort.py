# tests/integration/test_full_sort.py

import unittest
import shutil
from pathlib import Path
from unittest.mock import patch
from zenith_archive.main import main

class TestFullSort(unittest.TestCase):
    def setUp(self):
        self.source_dir = Path("test_source")
        self.docs_dir = Path("test_documents")
        self.log_file = Path("test_archive.log")

        # Create test directories and files
        self.source_dir.mkdir(exist_ok=True)
        self.docs_dir.mkdir(exist_ok=True)

        (self.source_dir / "document.pdf").touch()
        (self.source_dir / "image.jpg").touch()
        (self.source_dir / "archive.zip").touch()
        (self.source_dir / "ignored.txt").touch()

        # Create a test config
        self.config_path = Path("test_integration_config.yaml")
        with open(self.config_path, "w") as f:
            f.write("ignore_files:\n  - ignored.txt")


    def tearDown(self):
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.docs_dir)
        if self.log_file.exists():
            self.log_file.unlink()
        if self.config_path.exists():
            self.config_path.unlink()

    @patch("sys.argv", new_callable=list)
    def test_sorting_logic(self, mock_argv):
        mock_argv.extend([
            "zenith_archive/main.py",
            "--source", str(self.source_dir),
            "--docs", str(self.docs_dir),
            "--config", str(self.config_path),
            "--log-file", str(self.log_file),
        ])

        main()

        # Assertions
        self.assertTrue((self.docs_dir / "DOCUMENTS" / "document.pdf").exists())
        self.assertTrue((self.docs_dir / "PHOTOS" / "image.jpg").exists())
        self.assertTrue((self.docs_dir / "ARCHIVES" / "archive.zip").exists())
        self.assertFalse((self.docs_dir / "ignored.txt").exists())
        self.assertTrue((self.source_dir / "ignored.txt").exists()) # Should remain
        self.assertTrue(self.log_file.exists())

if __name__ == "__main__":
    unittest.main()
