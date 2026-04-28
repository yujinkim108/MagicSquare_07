"""Grid dimensions and domain sentinels — single source (PRD / Report/02)."""

from __future__ import annotations

# 4×4 magic square puzzle
MATRIX_SIZE: int = 4

# Cell value used for an empty cell in the input grid
CELL_EMPTY: int = 0

# Allowed value range for each cell in partial grid input
CELL_MIN_VALUE: int = 0
CELL_MAX_VALUE: int = 16

# Completed 4×4 magic square row/column/diagonal sum
MAGIC_SUM: int = 34

# Partial grid input must have exactly this many empty cells
EXPECTED_EMPTY_CELL_COUNT: int = 2
