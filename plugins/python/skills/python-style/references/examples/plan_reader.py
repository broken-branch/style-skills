# House rules: specific exception hierarchies and chained causes [PEP8];
# explicit text encoding, resource cleanup, and narrow catches [GOOGLE-PYTHON].
"""Read a UTF-8 plan containing a label line followed by an integer limit line."""

from pathlib import Path

from batch_plan import BatchPlan


class PlanError(Exception):
    """A failure to load a batch plan."""


class PlanReadError(PlanError):
    """A plan that could not be opened or read."""


class PlanFormatError(PlanError):
    """A plan whose text or values are invalid."""


def read_plan(path: Path) -> BatchPlan:
    """Read and validate one plan without changing the input file.

    Args:
        path: Exact path to a UTF-8 file with two lines and an optional final newline.

    Returns:
        The validated batch plan, preserving a supplied zero limit.

    Raises:
        PlanReadError: Opening or reading the file fails.
        PlanFormatError: The encoding, line count, label, or limit is invalid.
    """
    try:
        with path.open("r", encoding="utf-8") as stream:
            text = stream.read()
    except OSError as error:
        raise PlanReadError("Could not read the batch plan") from error
    except UnicodeError as error:
        raise PlanFormatError("The batch plan must be UTF-8") from error

    lines = text.splitlines()
    if len(lines) != 2:
        raise PlanFormatError("The batch plan must have exactly two lines")
    label, limit_text = lines
    try:
        limit = int(limit_text)
    except ValueError as error:
        raise PlanFormatError("The item limit must be an integer") from error
    try:
        return BatchPlan(label=label, limit=limit)
    except ValueError as error:
        raise PlanFormatError("The batch plan values are invalid") from error
