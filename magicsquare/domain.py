"""Pure domain logic — no UI, web, DB, or PyQt (Clean Architecture)."""

from __future__ import annotations

from typing import Tuple

from magicsquare.constants import CELL_EMPTY, MATRIX_SIZE

Coord = Tuple[int, int]


def find_blank_coords(grid: list[list[int]]) -> list[Coord]:
    """
    Return the two empty-cell coordinates in row-major (row asc, then col asc) order.
    Preconditions: grid is MATRIX_SIZE×MATRIX_SIZE and contains exactly two CELL_EMPTY values.
    Coordinates are 0-based indices into the grid.
    """
    found: list[Coord] = []
    for r in range(MATRIX_SIZE):
        for c in range(MATRIX_SIZE):
            if grid[r][c] == CELL_EMPTY:
                found.append((r, c))
    return found
