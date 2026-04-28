"""Additional domain tests for negative and failure scenarios."""

from __future__ import annotations

import pytest

import magicsquare.domain as domain_module
from magicsquare.domain import find_not_exist_nums, is_magic_square, solution


class TestDomainAdditional:
    def test_solution_raises_when_blank_count_is_not_two(self) -> None:
        no_blank_grid = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 6, 12],
            [4, 14, 15, 1],
        ]

        with pytest.raises(ValueError, match="Expected exactly two blank cells"):
            solution(no_blank_grid)

    def test_find_not_exist_nums_raises_when_missing_count_is_not_two(self) -> None:
        three_blanks = [
            [0, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 0],
        ]

        with pytest.raises(ValueError, match="Expected exactly two missing numbers"):
            find_not_exist_nums(three_blanks)

    def test_is_magic_square_false_when_row_sum_is_incorrect(self) -> None:
        not_magic = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 6, 12],
            [4, 14, 15, 2],
        ]

        assert is_magic_square(not_magic) is False

    def test_is_magic_square_false_when_values_are_duplicated(self) -> None:
        duplicated_values = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 6, 12],
            [4, 14, 15, 15],
        ]

        assert is_magic_square(duplicated_values) is False

    def test_is_magic_square_false_when_grid_is_not_4x4(self) -> None:
        not_4x4 = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 6, 12],
        ]

        assert is_magic_square(not_4x4) is False

    def test_is_magic_square_false_when_column_sum_is_incorrect(self) -> None:
        bad_column = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 6, 12],
            [1, 14, 15, 4],
        ]

        assert is_magic_square(bad_column) is False

    def test_is_magic_square_false_on_main_diagonal_branch(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        magic_square = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 6, 12],
            [4, 14, 15, 1],
        ]
        original_sum = sum
        calls = {"n": 0}

        def _fake_sum(iterable):  # type: ignore[no-untyped-def]
            calls["n"] += 1
            if calls["n"] == 9:
                return 33
            return original_sum(iterable)

        monkeypatch.setattr(domain_module, "sum", _fake_sum, raising=False)

        assert is_magic_square(magic_square) is False

    def test_is_magic_square_false_on_anti_diagonal_branch(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        magic_square = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 6, 12],
            [4, 14, 15, 1],
        ]
        original_sum = sum
        calls = {"n": 0}

        def _fake_sum(iterable):  # type: ignore[no-untyped-def]
            calls["n"] += 1
            if calls["n"] == 10:
                return 33
            return original_sum(iterable)

        monkeypatch.setattr(domain_module, "sum", _fake_sum, raising=False)

        assert is_magic_square(magic_square) is False

    def test_solution_returns_ordered_assignment_when_first_try_matches(self) -> None:
        partial = [
            [0, 15, 14, 4],
            [12, 6, 7, 9],
            [8, 10, 11, 5],
            [13, 3, 2, 0],
        ]

        result = solution(partial)
        assert result == [1, 1, 1, 4, 4, 16]

    def test_solution_raises_no_solution_when_both_assignments_fail(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        valid_shape = [
            [0, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0],
        ]
        monkeypatch.setattr(domain_module, "is_magic_square", lambda _grid: False)

        with pytest.raises(ValueError, match="NO_SOLUTION"):
            solution(valid_shape)
