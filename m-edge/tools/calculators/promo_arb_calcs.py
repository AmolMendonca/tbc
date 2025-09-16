# promo_arb_calcs.py
"""
Arbitrage & promo-related calculation stubs for M-Ed  ge.

All odds passed into these functions are expected to be **American odds** (ints),
consistent with the rest of the codebase. Callers should use the converters in
`converters.py` to transform formats as needed before/after calling.

This module provides:
- `arbitrage_possible`: quick boolean check on whether an arbitrage exists.
- `hv_calculator`: hedge-value calculator for a 2-way pair (assumes $100 on the underdog by default).
- `2way_arb_calculator`: two-way arbitrage margin and favorite bet-size for a $100 underdog stake by default.
- `nway_arb_calc`: generalized N-way arbitrage allocation and margin for a configurable total stake.

"""

from typing import Iterable, List, Tuple


def arbitrage_possible(american_odds: Iterable[int]) -> bool:
    """
    Return True if an arbitrage is possible, False otherwise.

    The canonical test (in decimal space) is:
        sum(1 / best_decimal_price_i) < 1  → arbitrage exists.

    Parameters
    ----------
    american_odds : Iterable[int]
        Iterable of **American** odds for the competing outcomes in the market
        (e.g., two-way ML, three-way soccer ML, etc.). Caller is responsible for
        ensuring these are the *best* prices across books for each outcome.

    Returns
    -------
    bool
        True if implied probabilities sum to less than 1.0 (i.e., an arbitrage),
        False otherwise.

    Notes
    -----
    - Conversion to decimal odds and implied probabilities should be handled
      internally (implementation to be added).
    - Caller may pre-aggregate “best line per outcome” before calling.
    """
    pass


def hv_calculator(
    udog_odds: int,
    favs_odds: int,
    base_udog_stake: float = 100.0,
) -> Tuple[float, float]:
    """
    Compute hedge value (HV) and the favorite bet size needed, given a
    **$100 default stake on the underdog** in a two-way (fully-covering) market.

    Parameters
    ----------
    udog_odds : int
        **American** odds for the underdog leg (positive if underdog, typically).
    favs_odds : int
        **American** odds for the opposing favorite leg (can be positive or negative).
    base_udog_stake : float, optional
        Dollar stake placed on the underdog. Defaults to 100.0.

    Returns
    -------
    Tuple[float, float]
        - hedge_value : float
            The hedge value (HV), i.e., profit as a fraction of `base_udog_stake`
            when positions are sized to lock in the same outcome across results.
            Conventionally reported as a proportion (e.g., 0.07 for +7%).
        - fav_bet_size : float
            The dollar amount to place on the favorite to achieve the hedge,
            given the `base_udog_stake` on the underdog.

    Notes
    -----
    - This mirrors the "matched betting" hedge sizing: size the favorite such that
      (net payoff if underdog wins) ≈ (net payoff if favorite wins).
    - Implementation must handle both +/- American odds correctly.
    """
    pass


def two_way_arb_calculator(
    udog_odds: int,
    favs_odds: int,
    base_udog_stake: float = 100.0,
) -> Tuple[float, float]:
    """
    Two-way arbitrage calculator for **American** odds.

    Parameters
    ----------
    udog_odds : int
        **American** odds for the underdog leg.
    favs_odds : int
        **American** odds for the favorite leg.
    base_udog_stake : float, optional
        Dollar stake placed on the underdog. Defaults to 100.0.

    Returns
    -------
    Tuple[float, float]
        - arb_margin : float
            Risk-free return as a fraction of total staked *or* as a fraction of
            `base_udog_stake` (implementation should document which; commonly
            reported relative to total stake). Example: 0.021 → +2.1%.
        - fav_bet_size : float
            Dollar amount to place on the favorite to lock the arbitrage given the
            underdog stake `base_udog_stake`.

    Notes
    -----
    - This function should explicitly compute a *guaranteed* profit sizing, then
      compute margin accordingly.
    - Implementation must handle sign conventions for American odds robustly.
    """
    pass


def nway_arb_calc(
    american_odds: Iterable[int],
    total_stake: float = 100.0,
) -> Tuple[float, List[float]]:
    """
    General N-way arbitrage allocation and margin for **American** odds.

    Parameters
    ----------
    american_odds : Iterable[int]
        Iterable of **American** odds for all mutually exclusive outcomes in the market
        (e.g., 3-way soccer ML, multi-runline menu, futures bucket, etc.).
        Caller should provide the best available price per outcome.
    total_stake : float, optional
        Total dollars to allocate across all outcomes for a (potential) guaranteed return.
        Defaults to 100.0.

    Returns
    -------
    Tuple[float, List[float]]
        - arb_margin : float
            Risk-free return as a fraction of `total_stake` if an arbitrage exists.
            Example: 0.015 → +1.5%. If no arb, implementation may return <= 0.
        - stakes : List[float]
            Dollar stakes to place on each outcome (same order as input) that
            equalize payoff across outcomes.

    Notes
    -----
    - Canonical allocation in decimal space uses stakes proportional to 1/price_i,
      normalized to match `total_stake`.
    - Implementation should verify arbitrage feasibility (sum of reciprocals < 1)
      and can return non-positive margins when not feasible.
    """
    pass
