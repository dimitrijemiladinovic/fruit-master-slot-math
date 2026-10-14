"""Checks for the Fruit Master model. Run:  python -m pytest   (or  python tests/test_model.py)"""
import itertools
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from slot_model import CYCLE, PAYTABLE, REELS, enumerate_cycle, evaluate  # noqa: E402
from enumerate_rtp import pay_for_target  # noqa: E402


def test_reels_have_20_stops():
    assert all(len(r) == 20 for r in REELS)
    assert CYCLE == 8000


def test_highest_win_is_paid():
    # Two wilds and a cherry qualify for CCC (4) and 2 Wilds (6): pay the higher one.
    assert evaluate('W', 'W', 'C') == ('2 Wilds', 6)
    # Two wilds and a lemon qualify for LLL (8) and 2 Wilds (6).
    assert evaluate('L', 'W', 'W') == ('LLL', 8)
    assert evaluate('W', 'W', 'W') == ('WWW', 80)
    assert evaluate('B', 'W', 'B') == ('BBB', 40)


def test_adding_a_symbol_never_lowers_the_win():
    # Replacing a blank with any symbol must not reduce the pay.
    for a, b, c in itertools.product(*REELS):
        base = evaluate(a, b, c)[1]
        for pos in range(3):
            spin = [a, b, c]
            if spin[pos] == '-':
                for sym in 'CLOB':
                    spin[pos] = sym
                    assert evaluate(*spin)[1] >= base, (a, b, c, spin)


def test_exact_values():
    r = enumerate_cycle()
    assert r['total_paid'] == 7679
    assert math.isclose(r['rtp'], 0.959875)
    assert math.isclose(r['hit_frequency'], 0.226125)
    assert r['max_win'] == 80
    assert sum(r['counts'].values()) == 1809


def test_balancing_hits_the_target():
    pay = pay_for_target('2 Wilds', 0.96)
    table = dict(PAYTABLE, **{'2 Wilds': pay})
    assert math.isclose(enumerate_cycle(table)['rtp'], 0.96)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
            print(f"{name}: ok")
