# ========================================================================
# This file is used for frameworks configuration. This is the
# beginning of frameworks configuration's layer.
# Also responsible for loading ".yaml" file.
# ========================================================================


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

    # =====================================================
    # Loads the configuration file.
    # =====================================================
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