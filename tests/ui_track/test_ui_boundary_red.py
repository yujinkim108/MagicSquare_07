"""Track A — UI / Boundary RED (Dual-Track). GREEN in progress per test.

Renamed from tests/boundary/ — avoids shadowing the ``boundary`` implementation package.
"""

from __future__ import annotations

import pytest

from boundary.errors import BoundaryError, ErrorCode
from boundary.validation import validate_4x4_shape


class TestUiBoundaryRed:
    """UI-RED-01 .. UI-RED-06. RED phase: every test must fail until GREEN."""

    def test_ui_red_01_not_4x4_raises(self) -> None:
        not_4x4 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]  # 3×4 — UI-SZ-01
        with pytest.raises(BoundaryError) as exc_info:
            validate_4x4_shape(not_4x4)
        assert exc_info.value.code is ErrorCode.INVALID_SIZE

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
