"""Track A — UI / Boundary RED (Dual-Track). Implementation intentionally absent."""

from __future__ import annotations

import pytest


class TestUiBoundaryRed:
    """UI-RED-01 .. UI-RED-06. RED phase: every test must fail until GREEN."""

    def test_ui_red_01_not_4x4_raises(self) -> None:
        pytest.fail("RED: not implemented")

    def test_ui_red_02_blank_count_not_two_raises(self) -> None:
        pytest.fail("RED: not implemented")

    def test_ui_red_03_value_out_of_range_raises(self) -> None:
        pytest.fail("RED: not implemented")

    def test_ui_red_04_duplicate_non_zero_raises(self) -> None:
        pytest.fail("RED: not implemented")

    def test_ui_red_05_success_payload_length_is_six(self) -> None:
        pytest.fail("RED: not implemented")

    def test_ui_red_06_success_coordinates_are_one_indexed(self) -> None:
        pytest.fail("RED: not implemented")
