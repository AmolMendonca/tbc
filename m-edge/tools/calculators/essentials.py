# essentials.py
"""
Core calculators (stubs) for M-Edge: Poisson tails, Parlay, and simple EV.

All functions below are **stubs** — implementations are intentionally omitted.
They define stable signatures, docstrings, and expected return formats so the
rest of the codebase can import and call them while implementations are added.

Conventions:
- American odds are integers (e.g., +145, -120).
- Probabilities are decimals in [0, 1].
"""

from typing import Iterable, Tuple, List, Literal, Optional


def poisson_tail_probability(
    lam: float,
    k: int,
    tail: Literal["gt", "ge", "lt", "le"] = "ge",
) -> float:
    """
    Compute a Poisson tail probability P(X ? k) where X ~ Poisson(lam).

    Parameters
    ----------
    lam : float
        The Poisson rate parameter λ (> 0), i.e., expected count.
    k : int
        Threshold count (>= 0).
    tail : {"gt","ge","lt","le"}, optional
        Which tail to compute:
          - "gt":  P(X >  k)
          - "ge":  P(X >= k)   (default)
          - "lt":  P(X <  k)
          - "le":  P(X <= k)

    Returns
    -------
    float
        The requested tail probability in [0, 1].

    Notes
    -----
    - Implementation should use stable cumulative calculations for large λ
      (e.g., incomplete gamma / scipy if available, or robust summation).
    """
    pass


def parlay_from_american(
    legs: Iterable[int],
) -> Tuple[float, int, float]:
    """
    Compute a parlay’s combined price and break-even probability under
    **independence** given leg prices in **American odds**.

    Parameters
    ----------
    legs : Iterable[int]
        American odds for each leg (e.g., [+130, -120, -105, +250]).

    Returns
    -------
    Tuple[float, int, float]
        - combined_decimal : float
            The combined **decimal odds** for the parlay.
        - combined_american : int
            The combined **American odds** (rounded to nearest int).
        - break_even_prob : float
            The parlay’s break-even probability in [0, 1].

    Assumptions
    -----------
    - Legs are independent.
    - Each leg is a single market outcome (no pushes/voids modeled here).

    Notes
    -----
    - Implementation should convert American→Decimal per leg, multiply to
      get the parlay price, then convert back to American and compute
      break-even as 1/combined_decimal.
    """
    pass


def ev_per_dollar(
    true_prob: float,
    american_odds: int,
) -> float:
    """
    Expected value per $1 stake given a **true win probability** and
    **American odds**.

    Parameters
    ----------
    true_prob : float
        The bettor’s true probability for the outcome (0 <= p <= 1).
    american_odds : int
        The offered American odds (e.g., +135, -110).

    Returns
    -------
    float
        EV per $1 staked (e.g., +0.07 means +$0.07 per $1 on average).

    Definition
    ----------
    EV = p * (payout_if_win) + (1 - p) * (loss_if_lose)

    Notes
    -----
    - For +A odds, payout_if_win = A/100 and loss_if_lose = -1.
    - For -B odds, payout_if_win = 100/B and loss_if_lose = -1.
    - Implementation should validate inputs (bounds on p, odds != 0).
    """
    pass
