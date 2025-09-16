# tester.py
from converters import (
    decimal_to_fractional,
    fractional_to_decimal,
    american_to_decimal,
    decimal_to_american,
    decimal_to_implied,
    implied_to_decimal,
)

from deviggers import devig_2way

# tester.py
 

TOL = 1e-9


def approx_equal(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol


def test_american_to_decimal():
    # +150 -> 2.5
    assert approx_equal(american_to_decimal(150), 2.5), "american_to_decimal(+150) should be 2.5"
    # -200 -> 1.5
    assert approx_equal(american_to_decimal(-250), 1.4), "american_to_decimal(-200) should be 1.5"


def test_decimal_to_american():
    # 2.5 -> +150
    assert decimal_to_american(2.5) == 150, "decimal_to_american(2.5) should be +150"
    # 1.5 -> -200
    assert decimal_to_american(1.5) == -200, "decimal_to_american(1.5) should be -200"


def test_decimal_implied_roundtrip():
    # 2.5 -> 0.4 -> 2.5
    p = decimal_to_implied(8.0)
    assert approx_equal(p, 0.125), "decimal_to_implied(8.0) should be 0.125"
    dec = implied_to_decimal(p)
    assert approx_equal(dec, 8.0), "implied_to_decimal(0.4) should be 2.5"


def test_fractional_decimal_roundtrip():
    # 2.5 -> 3/2 and back
    num, den = decimal_to_fractional(2.5)
    assert (num, den) == (3, 2), "decimal_to_fractional(2.5) should be (3,2)"
    dec = fractional_to_decimal(num, den)
    assert approx_equal(dec, 2.5), "fractional_to_decimal(3,2) should be 2.5"


def test_mixed_example():
    dec = american_to_decimal(-110)  # 100/110 + 1 = 1.9090909091
    assert approx_equal(dec, 1.9090909090909092), "american_to_decimal(-110) should be ~1.90909"
    p = decimal_to_implied(dec)      # ~0.5238095238
    assert approx_equal(p, 0.5238095238095238), "decimal_to_implied(1.90909) should be ~0.5238095"
    dec_back = implied_to_decimal(p)
    assert approx_equal(dec_back, dec), "implied_to_decimal(roundtrip) mismatch"

def test_devig_equal_priced_market():
    """
    -110 / -110 -> implied probs ~0.5238095 each, book ~1.047619, vig ~4.7619%.
    Additive devig -> 0.5 / 0.5 -> +100 / +100.
    """
    vig, o1, o2 = devig_2way(-110, -110, method="additive")
    assert approx_equal(vig, 4.76, tol=0.05), f"vig should be ~4.76%, got {vig}%"
    assert o1 == 100 and o2 == 100, f"devigged odds should be +100/+100, got {o1}/{o2}"

def test_devig_unequal_priced_market():
    """
    +120 / -140:
      p1 = 1/2.2 = 0.454545...
      p2 = 1/1.714285... = 0.583333...
      book ~ 1.037879 -> vig ~ 3.79%
      Additive devig normalizes to sum=1; odds likely around +128 / -128 (approx).
    Validate: (1) vig ~ 3.79%, (2) devigged implied probs sum ~1.
    """
    vig, o1, o2 = devig_2way(120, -140, method="additive")
    assert approx_equal(vig, 3.79, tol=0.1), f"vig should be ~3.79%, got {vig}%"

    # Convert back to implied and confirm sums to ~1.0
    d1 = american_to_decimal(o1)
    d2 = american_to_decimal(o2)
    p1 = decimal_to_implied(d1)
    p2 = decimal_to_implied(d2)
    assert approx_equal(p1 + p2, 1.0, tol=1e-6), f"vig-free probs should sum to 1.0, got {p1+p2}"

def test_devig_raises_for_unsupported_method():
    """
    Any method other than 'additive' should raise NotImplementedError.
    """
    for m in ("shin", "subtractive", "power"):
        raised = False
        try:
            devig_2way(-110, -110, method=m)
        except NotImplementedError:
            raised = True
        assert raised, f"Expected NotImplementedError for method='{m}'"

def test_devig_signs_and_reasonableness():
    """
    Spot-check a more lopsided pair:
      +200 / -250
      Ensure vig > 0 and final probs sum ~1 after devig.
    """
    vig, o1, o2 = devig_2way(200, -250, method="additive")
    assert vig > 0, f"vig should be > 0, got {vig}"

    d1 = american_to_decimal(o1)
    d2 = american_to_decimal(o2)
    p1 = decimal_to_implied(d1)
    p2 = decimal_to_implied(d2)
    assert approx_equal(p1 + p2, 1.0, tol=1e-6), f"vig-free probs should sum to 1.0, got {p1+p2}"

def test_devig_boundary_reasonable():
    """
    Check that a near-fair book (e.g., +101 / -101-ish) produces a small vig
    and near-original probabilities after devig.
    """
    vig, o1, o2 = devig_2way(101, -101, method="additive")
    # vig should be small but positive
    assert 0.0 <= vig < 2.0, f"vig should be small, got {vig}"

    # And devigged probs sum to ~1
    d1 = american_to_decimal(o1)
    d2 = american_to_decimal(o2)
    p1 = decimal_to_implied(d1)
    p2 = decimal_to_implied(d2)
    assert approx_equal(p1 + p2, 1.0, tol=1e-6), f"vig-free probs should sum to 1.0, got {p1+p2}"



def main():
    tests = [
        ("american_to_decimal", test_american_to_decimal),
        ("decimal_to_american", test_decimal_to_american),
        ("decimal/implied roundtrip", test_decimal_implied_roundtrip),
        ("fractional/decimal roundtrip", test_fractional_decimal_roundtrip),
        ("mixed example (-110)", test_mixed_example),

        # New devig tests
        ("devig equal-priced (-110/-110)", test_devig_equal_priced_market),
        ("devig unequal (+120/-140)", test_devig_unequal_priced_market),
        ("devig unsupported methods", test_devig_raises_for_unsupported_method),
        ("devig reasonableness (+200/-250)", test_devig_signs_and_reasonableness),
        ("devig boundary (+101/-101)", test_devig_boundary_reasonable),
    ]

    passed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"[PASS] {name}")
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {name}: {e}")

    print(f"\n{passed}/{len(tests)} tests passed.")


if __name__ == "__main__":
    main()