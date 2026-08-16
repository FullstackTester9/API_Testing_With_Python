# =====================================================
# The purpose of this file is to select the
# environment: dev or qa.
# In the PowerShell type: $env:TEST_ENV="qa" for
# selecting the environment.
# It creates an environment variable for your current
# PowerShell session.
# =====================================================
import os

from framework.config.config_loader import ConfigLoader


class EnvironmentManager:

    def __init__(self, environment=None):
        self.environment = (
            environment
            or os.getenv("TEST_ENV")
            or "qa"
        )

    # =====================================================
    # Loads the environment file.
    # "qa.yaml" or "dev.yaml"
    # =====================================================
    def load(self):
        config_loader = ConfigLoader()

        common_config = config_loader.load()

        environment_file = (
            config_loader.project_root
            / "config"
            / f"{self.environment}.yaml"
        )

        environment_config = ConfigLoader(
            environment_file
        ).load()

        return self._merge_configs(
            common_config,
            environment_config
        )

    # =====================================================
    # The class "EnvironmentManager" loads both the
    # "config.yaml" and "qa.yaml" results in a merged
    # dictionary available to tests
    # =====================================================
    @staticmethod
    def _merge_configs(common_config, environment_config):
        merged_config = common_config.copy()

        for key, value in environment_config.items():

            if (
                key in merged_config
                and isinstance(merged_config[key], dict)
                and isinstance(value, dict)
            ):
                merged_config[key].update(value)
            else:
                merged_config[key] = value

        return merged_config