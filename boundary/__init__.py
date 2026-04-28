"""Boundary (CLI / input schema) — ECB screen layer."""

from boundary.errors import BoundaryError, ErrorCode
from boundary.validation import validate_4x4_shape

__all__ = ["BoundaryError", "ErrorCode", "validate_4x4_shape"]
