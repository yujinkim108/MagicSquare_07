"""Track B — Logic RED (Dual-Track). GREEN per test group."""

from __future__ import annotations

import pytest

from magicsquare.constants import CELL_EMPTY, MATRIX_SIZE
from magicsquare.domain import find_blank_coords


class TestLogicRed:
    """LOGIC-RED-01 .. LOGIC-RED-04. RED phase: every test must fail until GREEN."""

    def test_logic_red_01_find_blank_coords_row_major_two_cells(self) -> None:
        grid = [
            [CELL_EMPTY, CELL_EMPTY, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]
        assert len(grid) == MATRIX_SIZE
        coords = find_blank_coords(grid)
        assert coords == [(0, 0), (0, 1)]

    def test_logic_red_02_find_not_exist_nums_two_sorted_asc(self) -> None:
        pytest.fail("RED: not implemented")

    def test_logic_red_03_is_magic_square_rows_cols_diags_sum_34(self) -> None:
        pytest.fail("RED: not implemented")

    def test_logic_red_04_solution_small_first_blank_then_reverse_six_tuple_one_based(
        self,
    ) -> None:
        pytest.fail("RED: not implemented")
