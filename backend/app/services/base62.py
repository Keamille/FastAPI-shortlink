"""Base62 helpers for short-code generation and custom-code validation.

Implement according to docs/DEVELOPMENT.md §3.2.
"""

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_SET = frozenset(ALPHABET)

# Case-insensitive reserved path segments that must not be used as short codes.
RESERVED_CODES = frozenset(
    {
        "api",
        "health",
        "docs",
        "redoc",
        "openapi",
        "static",
    }
)

CUSTOM_CODE_MIN_LEN = 3
CUSTOM_CODE_MAX_LEN = 32


def to_base62(n: int, min_length: int = 6) -> str:
    result = ""
    if n == 0:
        result = ALPHABET[0]
    else:
        while n > 0:
            n, i = divmod(n, len(ALPHABET))
            result = ALPHABET[i] + result
    return result.zfill(min_length)

def is_valid_custom_code(code: str) -> bool:
    """Return True if code matches Base62 charset, length, and is not reserved.

    Rules (docs §3.2.2):
    - charset: Base62 only
    - length: 3..32
    - not in RESERVED_CODES (case-insensitive)
    """
    if code.lower() in RESERVED_CODES:
        return False

    if len(code) < CUSTOM_CODE_MIN_LEN or len(code) > CUSTOM_CODE_MAX_LEN:
        return False

    if not all(c in ALPHABET_SET for c in code):
        return False

    return True
