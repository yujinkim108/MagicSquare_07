"""Additional boundary contract tests for edge cases and mapping."""

from __future__ import annotations

import pytest

import magicsquare.boundary as boundary_module
from magicsquare.boundary import BoundaryError, ErrorCode, solve, validate_4x4_shape


class TestBoundaryAdditional:
    def test_validate_4x4_shape_none_raises_invalid_size(self) -> None:
        with pytest.raises(BoundaryError) as exc_info:
            validate_4x4_shape(None)
        assert exc_info.value.code is ErrorCode.INVALID_SIZE

    def test_validate_4x4_shape_ragged_rows_raise_invalid_size(self) -> None:
        ragged = [
            [1, 2, 3, 4],
            [5, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15],
        ]
        with pytest.raises(BoundaryError) as exc_info:
            validate_4x4_shape(ragged)
        assert exc_info.value.code is ErrorCode.INVALID_SIZE

    def test_solve_maps_no_solution_value_error_to_boundary_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        valid_input = [
            [0, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0],
        ]

        def _raise_no_solution(_grid: list[list[int]]) -> list[int]:
            raise ValueError("NO_SOLUTION")

        monkeypatch.setattr(boundary_module, "solution", _raise_no_solution)

        with pytest.raises(BoundaryError) as exc_info:
            solve(valid_input)
        assert exc_info.value.code is ErrorCode.NO_SOLUTION

    def test_solve_re_raises_unexpected_value_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        valid_input = [
            [0, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0],
        ]

        def _raise_other_error(_grid: list[list[int]]) -> list[int]:
            raise ValueError("unexpected")

        monkeypatch.setattr(boundary_module, "solution", _raise_other_error)

        with pytest.raises(ValueError, match="unexpected"):
            solve(valid_input)

    def test_solve_runs_value_range_before_blank_count(self) -> None:
        # One out-of-range value and wrong blank count:
        # contract order must report INVALID_VALUE_RANGE first.
        invalid = [
            [0, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 17],
        ]

        with pytest.raises(BoundaryError) as exc_info:
            solve(invalid)
        assert exc_info.value.code is ErrorCode.INVALID_VALUE_RANGE
