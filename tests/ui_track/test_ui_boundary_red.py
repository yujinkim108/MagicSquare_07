"""Track A — UI / Boundary RED (Dual-Track). GREEN in progress per test.

Renamed from tests/boundary/ — avoids shadowing the ``boundary`` implementation package.
"""

from __future__ import annotations

import pytest

from magicsquare.boundary import (
    BoundaryError,
    ErrorCode,
    solve,
    validate_4x4_shape,
    validate_empty_cell_count,
    validate_no_duplicate_non_zero,
    validate_value_range,
)
from magicsquare.constants import CELL_EMPTY, MATRIX_SIZE


class TestUiBoundaryRed:
    """UI-RED-01 .. UI-RED-06. RED phase: every test must fail until GREEN."""

    def test_ui_red_01_not_4x4_raises(self) -> None:
        not_4x4 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]  # 3×4 — UI-SZ-01
        with pytest.raises(BoundaryError) as exc_info:
            validate_4x4_shape(not_4x4)
        assert exc_info.value.code is ErrorCode.INVALID_SIZE

    def test_ui_red_02_blank_count_not_two_raises(self) -> None:
        # 4×4 but sixteen empties — UI-BC-04
        all_empty = [[CELL_EMPTY] * 4 for _ in range(4)]
        with pytest.raises(BoundaryError) as exc_info:
            validate_empty_cell_count(all_empty)
        assert exc_info.value.code is ErrorCode.INVALID_BLANK_COUNT

    def test_ui_red_03_value_out_of_range_raises(self) -> None:
        out_of_range = [
            [CELL_EMPTY, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 17],
        ]
        with pytest.raises(BoundaryError) as exc_info:
            validate_value_range(out_of_range)
        assert exc_info.value.code is ErrorCode.INVALID_VALUE_RANGE

    def test_ui_red_04_duplicate_non_zero_raises(self) -> None:
        duplicated = [
            [CELL_EMPTY, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 5, CELL_EMPTY],
        ]
        with pytest.raises(BoundaryError) as exc_info:
            validate_no_duplicate_non_zero(duplicated)
        assert exc_info.value.code is ErrorCode.INVALID_DUPLICATE

    def test_ui_red_05_success_payload_length_is_six(self) -> None:
        partial = [
            [CELL_EMPTY, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 6, 12],
            [4, 14, 15, CELL_EMPTY],
        ]
        result = solve(partial)
        assert len(result) == 6

    def test_ui_red_06_success_coordinates_are_one_indexed(self) -> None:
        partial = [
            [CELL_EMPTY, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 6, 12],
            [4, 14, 15, CELL_EMPTY],
        ]
        result = solve(partial)
        row_1, col_1, _, row_2, col_2, _ = result
        assert 1 <= row_1 <= MATRIX_SIZE
        assert 1 <= col_1 <= MATRIX_SIZE
        assert 1 <= row_2 <= MATRIX_SIZE
        assert 1 <= col_2 <= MATRIX_SIZE
