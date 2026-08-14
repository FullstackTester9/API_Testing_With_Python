import pytest


@pytest.mark.smoke
def test_framework_configuration(config):
    assert config is not None
    assert "api" in config
    assert "base_url" in config["api"]

