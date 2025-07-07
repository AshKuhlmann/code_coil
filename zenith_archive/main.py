# zenith_archive/main.py

import argparse
from pathlib import Path
from . import config
from . import logger
from .archiver import Archiver

def main():
    parser = argparse.ArgumentParser(description="Zenith Archive - A file organizer.")
    parser.add_argument(
        "--source",
        type=Path,
        default=Path.cwd(),
        help="The source directory to sort. Defaults to the current directory.",
    )
    parser.add_argument(
        "--docs",
        type=Path,
        default=None,
        help="The main documents directory. Defaults to a 'DOCUMENTS' folder in the current directory.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.yaml"),
        help="Path to the configuration file.",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=Path("archive.log"),
        help="Path to the log file.",
    )
    args = parser.parse_args()

    # Setup
    app_logger = logger.setup_logger(args.log_file)
    app_config = config.load_config(args.config)
    rules = config.get_rules(app_config)

    documents_dir = args.docs or app_config.get("documents_dir")
    if documents_dir:
        documents_dir = Path(documents_dir)
    else:
        documents_dir = Path.cwd() / "DOCUMENTS"


    # Create and run the archiver
    archiver = Archiver(
        rules=rules,
        ignore_list=app_config.get("ignore_files", []),
        documents_dir=documents_dir,
        logger=app_logger,
    )
    archiver.sort_directory(args.source)
    print("Sorting complete. See archive.log for details.")

if __name__ == "__main__":
    main()
