# =====================================================
# This file checks the foundation of this framework.
# =====================================================


import pytest


# =====================================================
# The main purpose of this method is to test the
# frameworks foundation. This method does not
# call the API.
# =====================================================
@pytest.mark.smoke
def test_framework_configuration(config):
    assert config is not None
    assert "api" in config
    assert "base_url" in config["api"]

