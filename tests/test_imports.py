import sys

import pytest


@pytest.mark.skipif(sys.platform != "darwin", reason="Test only runs on macOS")
def test_imports_macos():
    from generalagents.macos import Computer

    assert Computer


def test_imports():
    from generalagents import Agent

    assert Agent
