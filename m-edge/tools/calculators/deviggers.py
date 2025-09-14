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

NOTE: These are stubs only; implementations are intentionally omitted.
"""

from typing import Iterable, List, Literal, Tuple


DevigMethod = Literal["additive", "subtractive", "power", "shin"]


def devig_2way(
    odds_a: int,
    odds_b: int,
    method: DevigMethod = "additive",
) -> Tuple[float, int, int]:
    """
    De-vig a 2-way market given **American** odds.

    Parameters
    ----------
    odds_a : int
        American odds for outcome A (may be positive or negative).
    odds_b : int
        American odds for outcome B (may be positive or negative).
    method : {'additive','subtractive','power','shin'}, optional
        De-vigging method to use. Defaults to 'additive'.

    Returns
    -------
    Tuple[float, int, int]
        A tuple:
        - vig_pct : float
            The implied overround (vig) as a percentage (e.g., 6.25 for 6.25%).
        - devig_a : int
            De-vigged **American** odds for outcome A (same order as input).
        - devig_b : int
            De-vigged **American** odds for outcome B (same order as input).

    Notes
    -----
    - Inputs MUST be American odds.
    - Returned odds are **American** odds.
    - Caller is responsible for any format conversions outside this function.
    """
    return 0


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
    pass
