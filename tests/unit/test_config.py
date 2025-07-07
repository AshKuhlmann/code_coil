# tests/unit/test_config.py

import unittest
from pathlib import Path
import yaml
from zenith_archive import config
from zenith_archive.constants import DEFAULT_RULES

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test_config_path = Path("test_config.yaml")
        self.custom_config = {
            "documents_dir": "/tmp/docs",
            "ignore_files": ["secret.txt"],
            "custom_rules": {"CUSTOM": [".custom"]},
        }
        with open(self.test_config_path, "w") as f:
            yaml.dump(self.custom_config, f)

    def tearDown(self):
        if self.test_config_path.exists():
            self.test_config_path.unlink()

    def test_load_config(self):
        loaded_config = config.load_config(self.test_config_path)
        self.assertEqual(loaded_config, self.custom_config)

    def test_load_nonexistent_config(self):
        config_data = config.load_config(Path("nonexistent.yaml"))
        self.assertIsNone(config_data["documents_dir"])
        self.assertIn(".DS_Store", config_data["ignore_files"])

    def test_get_rules_with_custom(self):
        rules = config.get_rules(self.custom_config)
        expected_rules = DEFAULT_RULES.copy()
        expected_rules.update(self.custom_config["custom_rules"])
        self.assertEqual(rules, expected_rules)

if __name__ == "__main__":
    unittest.main()
