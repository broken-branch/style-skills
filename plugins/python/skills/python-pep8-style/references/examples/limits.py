# PEP 8: public names, exception classes, narrow try blocks, explicit
# exception chaining, and 79-column code with 72-column prose [PEP8].
"""Parse nonnegative limits with a documented application exception."""

__all__ = ["LimitError", "parse_limit"]


class LimitError(ValueError):
    """A limit whose text or numeric range is invalid."""


def parse_limit(text):
    """Return the nonnegative integer represented by a string.

    Raise LimitError if text is not an integer or represents a negative
    value. Invalid integer text retains the ValueError as its cause.
    Whitespace and a leading plus sign follow int's parsing behavior.
    """
    try:
        value = int(text)
    except ValueError as error:
        raise LimitError("limit must be an integer") from error
    if value < 0:
        raise LimitError("limit must be nonnegative")
    return value
