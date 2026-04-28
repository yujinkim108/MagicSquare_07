"""Pure domain logic — no UI, web, DB, or PyQt (Clean Architecture)."""

from __future__ import annotations

from typing import Tuple

from magicsquare.constants import CELL_EMPTY, CELL_MAX_VALUE, MAGIC_SUM, MATRIX_SIZE

Coord = Tuple[int, int]


def _sum_row(grid: list[list[int]], row: int) -> int:
    return sum(grid[row])


def _sum_col(grid: list[list[int]], col: int) -> int:
    return sum(grid[row][col] for row in range(MATRIX_SIZE))


def _sum_main_diag(grid: list[list[int]]) -> int:
    return sum(grid[i][i] for i in range(MATRIX_SIZE))


def _sum_anti_diag(grid: list[list[int]]) -> int:
    return sum(grid[i][MATRIX_SIZE - 1 - i] for i in range(MATRIX_SIZE))


def _try_placement(
    grid: list[list[int]],
    first_blank: Coord,
    second_blank: Coord,
    first_value: int,
    second_value: int,
) -> list[int] | None:
    candidate = [row[:] for row in grid]
    candidate[first_blank[0]][first_blank[1]] = first_value
    candidate[second_blank[0]][second_blank[1]] = second_value
    if not is_magic_square(candidate):
        return None
    return [
        first_blank[0] + 1,
        first_blank[1] + 1,
        first_value,
        second_blank[0] + 1,
        second_blank[1] + 1,
        second_value,
    ]


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


def find_not_exist_nums(grid: list[list[int]]) -> tuple[int, int]:
    """Return the two missing numbers from 1..16 in ascending order."""
    present = set()
    for row in grid:
        for value in row:
            if value != CELL_EMPTY:
                present.add(value)

    missing = sorted(value for value in range(1, CELL_MAX_VALUE + 1) if value not in present)
    if len(missing) != 2:
        raise ValueError("Expected exactly two missing numbers")
    return missing[0], missing[1]


def is_magic_square(grid: list[list[int]]) -> bool:
    """Check if a completed 4×4 grid is a valid magic square."""
    values = [cell for row in grid for cell in row]
    expected_values = set(range(1, CELL_MAX_VALUE + 1))
    if len(values) != MATRIX_SIZE * MATRIX_SIZE:
        return False
    if set(values) != expected_values:
        return False

    for r in range(MATRIX_SIZE):
        if _sum_row(grid, r) != MAGIC_SUM:
            return False
    for c in range(MATRIX_SIZE):
        if _sum_col(grid, c) != MAGIC_SUM:
            return False

    if _sum_main_diag(grid) != MAGIC_SUM:
        return False
    if _sum_anti_diag(grid) != MAGIC_SUM:
        return False
    return True


def solution(grid: list[list[int]]) -> list[int]:
    """
    Fill two blanks with missing numbers using contract order:
    smaller -> first blank, larger -> second, then reverse fallback.
    Return 1-indexed payload [r1, c1, n1, r2, c2, n2].
    """
    blanks = find_blank_coords(grid)
    if len(blanks) != 2:
        raise ValueError("Expected exactly two blank cells")
    first_blank, second_blank = blanks
    smaller, larger = find_not_exist_nums(grid)

    ordered = _try_placement(grid, first_blank, second_blank, smaller, larger)
    if ordered is not None:
        return ordered

    reversed_order = _try_placement(grid, first_blank, second_blank, larger, smaller)
    if reversed_order is not None:
        return reversed_order
    raise ValueError("NO_SOLUTION")
