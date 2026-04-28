"""Error contract for boundary (Report/02 ErrorContract)."""

from __future__ import annotations

from enum import Enum


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
