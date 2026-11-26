# PEP 257: raw docstrings, imperative one-line summaries, and an exported
# function inventory in the module docstring [PEP257].
"""Provide helpers for displaying control characters.

escape_tabs: Replace tab characters with a visible escape sequence.
"""


def escape_tabs(text):
    r"""Return text with each tab replaced by the two characters \t."""
    return text.replace("\t", r"\t")
