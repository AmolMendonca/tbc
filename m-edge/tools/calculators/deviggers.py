# devigger.py
"""
Devigging utilities for M-Edge.

This module defines stubs for de-vigging (overround removal) across 2-way and N-way
markets. **Inputs are American odds only**. Callers are expected to handle any
format conversions before/after using these functions.

Supported methods (select via `method` arg):
- "additive"    : proportional normalization / standard overround removal
- "subtractive" : simple subtraction-based normalization
- "power"       : power method fit
- "shin"        : Shin’s method for insider trading bias

"""

from typing import Iterable, List, Literal, Tuple
from converters import decimal_to_american, american_to_decimal, decimal_to_implied, implied_to_decimal



DevigMethod = Literal["additive", "subtractive", "power", "shin"]



def devig_2way(odds1: int, odds2: int, method: str = "additive") -> Tuple[float, int, int]:
    """
    De-vig a 2-way market given American odds using the specified method.

    Args:
        odds1 (int): American odds for outcome 1.
        odds2 (int): American odds for outcome 2.
        method (str): De-vigging method. Supported: "additive".
                      Others ("shin", "subtractive", "power") will raise for now.

    Returns:
        Tuple[float, int, int]: (vig_percent, devigged_odds1, devigged_odds2)
            - vig_percent: Overround as a percentage (e.g., 7.0 for a 1.07 book).
            - devigged_odds1: Vig-free American odds for outcome 1.
            - devigged_odds2: Vig-free American odds for outcome 2.

    Raises:
        ValueError: If inputs are invalid or normalization fails.
        NotImplementedError: If method is not available yet.
    """
    if method.lower() != "additive":
        raise NotImplementedError(f"{method} method not available yet")

    # Convert American -> Decimal -> Implied
    dec1 = american_to_decimal(odds1)
    dec2 = american_to_decimal(odds2)

    if dec1 <= 1.0 or dec2 <= 1.0:
        raise ValueError("Decimal odds must be > 1.0 after conversion from American.")

    p1 = decimal_to_implied(dec1)  # = 1/dec1
    p2 = decimal_to_implied(dec2)  # = 1/dec2

    # Total book and vig (as %)
    book = p1 + p2
    if book <= 0:
        raise ValueError("Invalid probabilities: sum(book) <= 0.")

    vig_percent = (book - 1.0) * 100.0

    
    p1_vf = p1 / book
    p2_vf = p2 / book

    d1_vf = implied_to_decimal(p1_vf)   # = 1/p1_vf
    d2_vf = implied_to_decimal(p2_vf)   # = 1/p2_vf

    if d1_vf <= 1.0 or d2_vf <= 1.0:
        raise ValueError("Vig-free decimal odds must be > 1.0.")

    o1_vf = decimal_to_american(d1_vf)
    o2_vf = decimal_to_american(d2_vf)

    return round(vig_percent, 2), o1_vf, o2_vf


# only ready for additive
def devig_nway(
    odds: Iterable[int],
    method: DevigMethod = "additive",
) -> Tuple[float, List[int]]:
    """
    De-vig an N-way market given **American** odds.

    Parameters
    ----------
    odds : Iterable[int]
        Iterable of American odds for all outcomes (length >= 2).
        Order is preserved and reflected in the output.
    method : {'additive','subtractive','power','shin'}, optional
        De-vigging method to use. Defaults to 'additive'.

    Returns
    -------
    Tuple[float, List[int]]
        A tuple:
        - vig_pct : float
            The implied overround (vig) as a percentage (e.g., 8.1 for 8.1%).
        - devigged_odds : List[int]
            List of de-vigged **American** odds for each outcome, in the same
            order as the input.

    Notes
    -----
    - Inputs MUST be American odds.
    - Returned odds are **American** odds.
    - Caller is responsible for any format conversions outside this function.
    """
    if method != "additive":
        raise NotImplementedError(f"Method '{method}' not available yet.")

    implied_probs = []
    for o in odds:
        dec = american_to_decimal(o)
        implied = decimal_to_implied(dec)
        implied_probs.append(implied)

    total_book = sum(implied_probs)

    vig_pct = (total_book - 1.0) * 100

    devigged_probs = [p / total_book for p in implied_probs]

    devigged_odds = []
    for p in devigged_probs:
        dec = implied_to_decimal(p)
        am = decimal_to_american(dec)
        devigged_odds.append(am)

    return vig_pct, devigged_odds
