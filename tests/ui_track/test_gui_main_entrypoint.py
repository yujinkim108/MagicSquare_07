"""Tests for GUI module entrypoint (python -m magicsquare.gui)."""

from __future__ import annotations

import runpy

import pytest

import magicsquare.gui.app as app_module


class TestGuiMainEntrypoint:
    def test_main_module_exits_with_run_return_code(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(app_module, "run", lambda: 3)

        with pytest.raises(SystemExit) as exc_info:
            runpy.run_module("magicsquare.gui.__main__", run_name="__main__")

        assert exc_info.value.code == 3
