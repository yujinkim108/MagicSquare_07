"""Boundary: input validation and error contract (Screen/CLI call this before domain)."""

from __future__ import annotations

from enum import Enum
from typing import Any

from magicsquare.constants import CELL_EMPTY, EXPECTED_EMPTY_CELL_COUNT, MATRIX_SIZE


class ErrorCode(str, Enum):
    INVALID_SIZE = "INVALID_SIZE"
    INVALID_BLANK_COUNT = "INVALID_BLANK_COUNT"
    INVALID_VALUE_RANGE = "INVALID_VALUE_RANGE"
    INVALID_DUPLICATE = "INVALID_DUPLICATE"
    NO_SOLUTION = "NO_SOLUTION"


class BoundaryError(Exception):
    def __init__(self, code: ErrorCode, message: str = "") -> None:
        self.code = code
        super().__init__(message or code.value)


def validate_4x4_shape(grid: Any) -> None:
    """
    Report/02: null, ragged, or wrong dimensions → INVALID_SIZE.
    """
    if grid is None:
        raise BoundaryError(ErrorCode.INVALID_SIZE)
    if not isinstance(grid, list) or len(grid) != MATRIX_SIZE:
        raise BoundaryError(ErrorCode.INVALID_SIZE)
    for row in grid:
        if not isinstance(row, list) or len(row) != MATRIX_SIZE:
            raise BoundaryError(ErrorCode.INVALID_SIZE)


def validate_empty_cell_count(grid: list[list[int]]) -> None:
    """
    After shape is valid: count of CELL_EMPTY must be EXPECTED_EMPTY_CELL_COUNT.
    Report/02 order — size before blank count.
    """
    count = 0
    for r in range(MATRIX_SIZE):
        for c in range(MATRIX_SIZE):
            if grid[r][c] == CELL_EMPTY:
                count += 1
    if count != EXPECTED_EMPTY_CELL_COUNT:
        raise BoundaryError(ErrorCode.INVALID_BLANK_COUNT)
