# Google Python: module imports, typed public APIs, and descriptive summaries
# with Args and Returns sections [GOOGLE-PYTHON].
"""Count whitespace-separated words with count_words(lines)."""

import collections
from collections.abc import Iterable


def count_words(lines: Iterable[str]) -> dict[str, int]:
    """Counts words without changing the supplied lines.

    Args:
        lines: Text lines, consumed once. Case is folded; punctuation is kept.

    Returns:
        A mapping from each folded word to its number of occurrences.
        Empty input produces an empty mapping.
    """
    counts: collections.Counter[str] = collections.Counter()
    for line in lines:
        counts.update(line.casefold().split())
    return dict(counts)
