from pathlib import Path

import yaml


class ConfigLoader:

    def __init__(self, config_file=None):
        project_root = Path(__file__).resolve().parents[2]

        self.project_root = project_root

        if config_file is None:
            config_file = project_root / "config" / "config.yaml"
        else:
            config_file = Path(config_file)

        self.config_file = config_file

    def load(self):
        if not self.config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_file}"
            )

        with self.config_file.open(
            "r",
            encoding="utf-8"
        ) as file:
            return yaml.safe_load(file)