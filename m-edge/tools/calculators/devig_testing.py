from typing import Iterable, List, Literal, Tuple
from converters import decimal_to_american, american_to_decimal, decimal_to_implied, implied_to_decimal


DevigMethod = str

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

    # Step 1: Convert each American odd -> implied probability
    implied_probs = []
    for o in odds:
        dec = american_to_decimal(o)
        implied = decimal_to_implied(dec)
        implied_probs.append(implied)

    # Step 2: Compute total book
    total_book = sum(implied_probs)

    # Step 3: Vig percentage (overround)
    vig_pct = (total_book - 1.0) * 100

    # Step 4: Normalize probs (divide each by total_book)
    devigged_probs = [p / total_book for p in implied_probs]

    # Step 5: Convert back to American odds
    devigged_odds = []
    for p in devigged_probs:
        dec = implied_to_decimal(p)
        am = decimal_to_american(dec)
        devigged_odds.append(am)

    return vig_pct, devigged_odds



vig_pct, deviggedline = devig_nway(odds=[-240, 350, 600], method="additive")

print(F"Vig percentage is {vig_pct} and devigged_line is {deviggedline}")