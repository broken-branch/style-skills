# PEP 257: class contracts, constructor documentation, keyword parameters,
# side effects, and exceptions in multiline docstrings [PEP257].
"""Provide Counter, a mutable nonnegative integer counter."""


class Counter:
    """Track an integer total through the public value attribute.

    advance adds to the total and returns the updated value. Assigning
    value directly is permitted only with a nonnegative integer. This
    class defines no separate interface for subclasses.
    """

    def __init__(self, start=0):
        """Initialize the counter from an integer.

        start: Optional initial value, defaulting to zero. This name may
            be used as a keyword argument.

        Raise ValueError if start is negative.
        """
        if start < 0:
            raise ValueError("start must be nonnegative")
        self.value = start

    def advance(self, amount=1):
        """Increase value and return the new integer total.

        amount: Optional nonnegative integer increment, defaulting to one.
            This name may be used as a keyword argument.

        Raise ValueError for a negative amount, leaving value unchanged.
        An amount of zero leaves value unchanged and returns its total.
        """
        if amount < 0:
            raise ValueError("amount must be nonnegative")
        self.value += amount
        return self.value
