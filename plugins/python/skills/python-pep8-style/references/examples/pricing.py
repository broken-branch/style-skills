# PEP 8: explicit exports, direct class imports, None identity checks,
# optional annotations, and breaks before binary operators [PEP8].
"""Calculate a total from decimal amounts without rounding them."""

__all__ = ["total_price"]

from decimal import Decimal


def total_price(subtotal, tax, *, shipping=None, discount=Decimal("0")):
    """Return the total of the supplied Decimal amounts.

    Use a shipping charge of 4.50 when shipping is None. A supplied zero
    means free shipping. Callers provide all other amounts as Decimals.
    """
    if shipping is None:
        shipping = Decimal("4.50")
    return (
        subtotal
        + tax
        + shipping
        - discount
    )
