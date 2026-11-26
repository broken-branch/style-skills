# House rules: typed boundaries and explicit runtime validation [GOOGLE-PYTHON];
# documented public data and imperative method summaries [PEP257] [MYPY].
"""A small validated batch plan."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BatchPlan:
    """An immutable label and item limit.

    Attributes:
        label: Nonblank text with at most 80 characters, preserved as supplied.
        limit: Maximum item count from zero through 1000; zero disables the batch.

    Raises:
        TypeError: The limit is a boolean rather than an item count.
        ValueError: The label or limit is outside its allowed range.
    """

    label: str
    limit: int = 100

    def __post_init__(self) -> None:
        """Enforce the label and item-count invariants."""
        if not self.label.strip() or len(self.label) > 80:
            raise ValueError("The label must contain 1 to 80 characters")
        if isinstance(self.limit, bool):
            raise TypeError("The item limit must not be a boolean")
        if not 0 <= self.limit <= 1000:
            raise ValueError("The item limit must be between 0 and 1000")
