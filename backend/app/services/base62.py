"""Base62 helpers for short-code generation.

Implement `to_base62` according to docs/DEVELOPMENT.md.
"""

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def to_base62(n: int, min_length: int = 6) -> str:
    """Convert a non-negative integer to a Base62 string with minimum length."""
    raise NotImplementedError("Implement Base62 encoding (see docs/DEVELOPMENT.md)")
