"""Input schema validation (Report/02 — size before value/blank/duplicate)."""

from __future__ import annotations

from typing import Any

from boundary.errors import BoundaryError, ErrorCode


def validate_4x4_shape(grid: Any) -> None:
    """
    Ensure the input is a 4×4 matrix (4 rows, each row length 4).
    Report/02: null, ragged, or wrong dimensions → INVALID_SIZE.
    """
    if grid is None:
        raise BoundaryError(ErrorCode.INVALID_SIZE)
    if not isinstance(grid, list) or len(grid) != 4:
        raise BoundaryError(ErrorCode.INVALID_SIZE)
    for row in grid:
        if not isinstance(row, list) or len(row) != 4:
            raise BoundaryError(ErrorCode.INVALID_SIZE)
