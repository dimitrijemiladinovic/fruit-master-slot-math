"""
Fruit Master v1.1 - the game model, shared by the enumeration and the simulation.

3 reels, 20 stops each, one payline, bet = 1.
A spin pays the HIGHEST qualifying win only (one payout per spin).
"""
import itertools
import math

REELS = [
    ['C', 'C', 'C', 'C', 'L', 'L', 'L', 'O', 'O', 'B', 'C', 'C', 'L', 'L', 'O', 'O', 'B', 'W', '-', '-'],
    ['C', 'C', 'C', 'L', 'L', 'L', 'O', 'O', 'O', 'B', 'C', 'L', 'L', 'O', 'O', 'B', 'W', '-', '-', '-'],
    ['C', 'C', 'L', 'L', 'L', 'O', 'O', 'O', 'B', 'B', 'C', 'L', 'O', 'O', 'B', 'W', '-', '-', '-', '-'],
]

WILD = 'W'

# Category -> pay (in bets). Order only matters for ties: the first listed wins.
PAYTABLE = {
    'WWW': 80,
    'BBB': 40,       # each reel B or W
    'OOO': 16,       # each reel O or W
    'LLL': 8,        # each reel L or W
    '2 Wilds': 6,    # exactly two wilds
    'CCC': 4,        # each reel C or W
    '1 Wild': 1,     # exactly one wild, anywhere
    'CC any': 1,     # reel 1 = C and reel 2 = C
}

CYCLE = math.prod(len(r) for r in REELS)  # 8,000


def qualifying_wins(s1, s2, s3, paytable=PAYTABLE):
    """Every category this outcome qualifies for, as (category, pay)."""
    symbols = (s1, s2, s3)
    n_wild = symbols.count(WILD)
    wins = []
    if n_wild == 3:
        wins.append('WWW')
    for sym in ('B', 'O', 'L', 'C'):
        if n_wild < 3 and all(s in (sym, WILD) for s in symbols):
            wins.append(sym * 3)
    if n_wild == 2:
        wins.append('2 Wilds')
    if n_wild == 1:
        wins.append('1 Wild')
    if s1 == 'C' and s2 == 'C':
        wins.append('CC any')
    return [(w, paytable[w]) for w in wins]


def evaluate(s1, s2, s3, paytable=PAYTABLE):
    """Return (category, pay) for the highest qualifying win, or (None, 0)."""
    best = (None, 0)
    for cat, pay in qualifying_wins(s1, s2, s3, paytable):
        if pay > best[1]:
            best = (cat, pay)
    return best


def enumerate_cycle(paytable=PAYTABLE):
    """Full enumeration of the cycle.

    Returns a dict with RTP, hit frequency, sigma, max win and,
    per category, the number of outcomes paid as that category.
    """
    counts = {cat: 0 for cat in paytable}
    total = total_sq = hits = max_win = 0
    for s1, s2, s3 in itertools.product(*REELS):
        cat, pay = evaluate(s1, s2, s3, paytable)
        if cat is not None:
            counts[cat] += 1
            hits += 1
        total += pay
        total_sq += pay * pay
        max_win = max(max_win, pay)
    rtp = total / CYCLE
    sigma = math.sqrt(total_sq / CYCLE - rtp ** 2)
    return {
        'rtp': rtp,
        'hit_frequency': hits / CYCLE,
        'sigma': sigma,
        'max_win': max_win,
        'total_paid': total,
        'counts': counts,
    }


def payout_table(paytable=PAYTABLE):
    """3-D table pay[i][j][k] for reel stops i, j, k (used by the fast simulation)."""
    return [[[evaluate(a, b, c, paytable)[1] for c in REELS[2]] for b in REELS[1]] for a in REELS[0]]
