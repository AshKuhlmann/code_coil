# zenith_archive/logger.py

import logging
from pathlib import Path

def setup_logger(log_file: Path = Path("archive.log")) -> logging.Logger:
    """Sets up a logger to log file operations."""
    logger = logging.getLogger("zenith_archive")
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if the function is called more than once
    if not logger.handlers:
        # Ensure log_file is an absolute path
        log_file = log_file.resolve()
        # Create file handler
        fh = logging.FileHandler(str(log_file))
        fh.setLevel(logging.INFO)

        # Create formatter and add it to the handler
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fh.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(fh)

    return logger
