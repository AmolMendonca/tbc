# converters.py
"""
Converters module for M-Edge tools.
"""

from fractions import Fraction
from typing import Tuple

# fraction return as numerator, denominator pair
def decimal_to_fractional(decimal_odds: float) -> Tuple[int, int]:
    """
    Convert decimal odds to fractional odds.

    Args:
        decimal_odds (float): Decimal odds value (> 1.0).

    Returns:
        Tuple[int, int]: Fractional odds (numerator, denominator).
    """
    if decimal_odds <= 1.0:
        raise ValueError("Decimal odds must be greater than 1.0")
    frac = Fraction(decimal_odds - 1).limit_denominator()
    return frac.numerator, frac.denominator


def fractional_to_decimal(numerator: int, denominator: int) -> float:
    """
    Convert fractional odds to decimal odds.

    Args:
        numerator (int): Numerator of fractional odds.
        denominator (int): Denominator of fractional odds.

    Returns:
        float: Decimal odds.
    """
    if denominator <= 0:
        raise ValueError("Denominator must be positive")
    return (numerator / denominator) + 1.0


def american_to_decimal(american_odds: int) -> float:
    """
    Convert American odds to decimal odds.

    Args:
        american_odds (int): American odds (positive or negative).

    Returns:
        float: Decimal odds.
    """
    if american_odds == 0:
        raise ValueError("American odds cannot be 0")
    if american_odds > 0:
        return (american_odds / 100.0) + 1.0
    else:
        return (100.0 / abs(american_odds)) + 1.0


def decimal_to_american(decimal_odds: float) -> int:
    """
    Convert decimal odds to American odds.

    Args:
        decimal_odds (float): Decimal odds value.

    Returns:
        int: American odds (positive or negative).
    """
    if decimal_odds < 1.0:
        raise ValueError("Decimal odds must be >= 1.0")
    if decimal_odds >= 2.0:
        return int((decimal_odds - 1.0) * 100)
    else:
        return int(-100 / (decimal_odds - 1.0))


def decimal_to_implied(decimal_odds: float) -> float:
    """
    Convert decimal odds to implied probability.

    Args:
        decimal_odds (float): Decimal odds value.

    Returns:
        float: Implied probability (0 to 1).
    """
    if decimal_odds <= 1.0:
        raise ValueError("Decimal odds must be greater than 1.0")
    return 1.0 / decimal_odds


def implied_to_decimal(implied_prob: float) -> float:
    """
    Convert implied probability to decimal odds.

    Args:
        implied_prob (float): Implied probability (0 to 1).

    Returns:
        float: Decimal odds value.
    """
    if implied_prob <= 0 or implied_prob > 1:
        raise ValueError("Implied probability must be in (0, 1]")
    return 1.0 / implied_prob
