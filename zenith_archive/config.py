# zenith_archive/config.py

import yaml
from pathlib import Path
from typing import Dict, Any, List
from .constants import DEFAULT_RULES

def load_config(config_path: Path = Path("config.yaml")) -> Dict[str, Any]:
    """Loads configuration from a YAML file."""
    if not config_path.is_file():
        return {
            "documents_dir": None,
            "ignore_files": [".DS_Store", "thumbs.db"],
            "custom_rules": {},
        }
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_rules(config: Dict[str, Any]) -> Dict[str, List[str]]:
    """Merges default rules with custom rules from the config."""
    rules = DEFAULT_RULES.copy()
    custom_rules = config.get("custom_rules", {})
    rules.update(custom_rules)
    return rules
