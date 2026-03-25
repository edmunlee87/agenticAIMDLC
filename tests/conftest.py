"""Shared pytest fixtures for the agentic MDLC platform test suite."""

import os
import pytest


CONFIGS_ROOT = os.path.join(os.path.dirname(__file__), "..", "configs", "runtime")


@pytest.fixture(scope="session")
def configs_root() -> str:
    """Return the absolute path to the runtime configs directory."""
    return os.path.abspath(CONFIGS_ROOT)
