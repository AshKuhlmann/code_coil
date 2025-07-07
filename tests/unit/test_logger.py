# tests/unit/test_logger.py

import unittest
import logging
from pathlib import Path
from zenith_archive.logger import setup_logger

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.log_file = Path("test_archive.log").resolve() # Make path absolute
        # Ensure the log file does not exist before each test
        if self.log_file.exists():
            self.log_file.unlink()
        # Clean up logger handlers before each test
        logger = logging.getLogger("zenith_archive")
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    def tearDown(self):
        # Clean up the log file after each test
        if self.log_file.exists():
            self.log_file.unlink()
        # Remove handlers to prevent issues with multiple test runs
        logger = logging.getLogger("zenith_archive")
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    def test_setup_logger(self):
        logger = setup_logger(self.log_file)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "zenith_archive")
        self.assertEqual(logger.level, logging.INFO)
        self.assertTrue(any(isinstance(h, logging.FileHandler) for h in logger.handlers))

        # Test that calling setup_logger again doesn't add duplicate handlers
        initial_handlers_count = len(logger.handlers)
        logger2 = setup_logger(self.log_file)
        self.assertEqual(len(logger2.handlers), initial_handlers_count)

        logger.info("Test log message") # Write a log message

        # Ensure the log is written to disk immediately
        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.flush()
                handler.close() # Explicitly close the handler

        # Check if the file exists before trying to open it
        self.assertTrue(self.log_file.exists(), "Log file was not created.")

        with open(self.log_file, "r") as f:
            content = f.read()
            self.assertIn("Test log message", content)

if __name__ == "__main__":
    unittest.main()