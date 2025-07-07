# zenith_archive/archiver.py

import shutil
from pathlib import Path
from typing import Dict, List
import logging

class Archiver:
    def __init__(
        self,
        rules: Dict[str, List[str]],
        ignore_list: List[str],
        documents_dir: Path,
        logger: logging.Logger,
    ):
        self.rules = self._invert_rules(rules)
        self.ignore_list = ignore_list
        self.documents_dir = documents_dir
        self.logger = logger

    @staticmethod
    def _invert_rules(rules: Dict[str, List[str]]) -> Dict[str, str]:
        """Inverts the rules mapping from {directory: [extensions]} to {extension: directory}."""
        inverted = {}
        for directory, extensions in rules.items():
            for ext in extensions:
                inverted[ext.lower()] = directory
        return inverted

    def sort_directory(self, source_dir: Path):
        """Sorts all files in the source directory according to the rules."""
        if not source_dir.is_dir():
            self.logger.error(f"Source directory not found: {source_dir}")
            return

        for file_path in source_dir.iterdir():
            if file_path.is_dir() or file_path.name in self.ignore_list:
                continue

            self._sort_file(file_path)

    def _sort_file(self, file_path: Path):
        """Sorts a single file."""
        extension = file_path.suffix.lower()
        if not extension:
            self.logger.warning(f"File has no extension, skipping: {file_path.name}")
            return

        target_dir_name = self.rules.get(extension)

        if not target_dir_name:
            self.logger.info(
                f"No rule found for extension '{extension}', skipping: {file_path.name}"
            )
            return

        # Handle special case for .iso files
        if extension == ".iso":
            if "install" in file_path.name.lower():
                target_dir_name = "SYSTEM_ADMIN"
            else:
                target_dir_name = "DATA"

        # Handle special case for .webm files (assuming A1 encoding check is complex)
        if extension == ".webm":
             # Placeholder for A1 encoding check
            target_dir_name = "VIDEO"

        # Handle special case for .py scripts
        if extension == ".py":
            # Simple check for short scripts
            if file_path.stat().st_size < 1024 * 5: # less than 5KB
                target_dir_name = "SYSTEM_ADMIN"


        destination_dir = self.documents_dir / target_dir_name
        destination_dir.mkdir(parents=True, exist_ok=True)

        destination_path = destination_dir / file_path.name
        try:
            shutil.move(str(file_path), str(destination_path))
            self.logger.info(f"Moved: {file_path} -> {destination_path}")
        except Exception as e:
            self.logger.error(f"Failed to move {file_path}: {e}")
