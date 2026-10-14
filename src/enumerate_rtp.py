"""
Fruit Master v1.1 - exact theoretical math by full enumeration of the 8,000-outcome cycle.

Prints a PAR-style table (hits, probability, pay and RTP contribution per category),
RTP, hit frequency, standard deviation and volatility index, and shows how to
balance a pay to a target RTP directly instead of by trial and error.
"""
from slot_model import CYCLE, PAYTABLE, enumerate_cycle

Z90, Z95 = 1.645, 1.96


def pay_for_target(category, target_rtp, paytable=PAYTABLE, max_steps=10):
    """Pay for `category` (a real number) that gives `target_rtp`.

    RTP is linear in each pay *as long as the same outcomes are paid as that
    category*: one unit of pay adds hits / CYCLE to the RTP. Because a spin pays
    only its highest win, changing a pay can move outcomes between categories,
    so the linear step is repeated until the category counts stop changing.
    """
    table = dict(paytable)
    for _ in range(max_steps):
        result = enumerate_cycle(table)
        hits = result['counts'][category]
        if hits == 0:
            raise ValueError(f"no outcomes are paid as {category!r}")
        new_pay = table[category] + (target_rtp - result['rtp']) * CYCLE / hits
        if abs(new_pay - table[category]) < 1e-12:
            return new_pay
        table[category] = new_pay
    return table[category]


def print_par(paytable=PAYTABLE):
    r = enumerate_cycle(paytable)
    print("=== Fruit Master v1.1 - full enumeration ===")
    print(f"Outcomes in cycle: {CYCLE:,}")
    print()
    print(f"{'Category':<10}{'Hits':>7}{'Probability':>14}{'Pay':>6}{'RTP contrib.':>14}")
    for cat, pay in paytable.items():
        hits = r['counts'][cat]
        p = hits / CYCLE
        print(f"{cat:<10}{hits:>7}{p:>14.6f}{pay:>6}{p * pay:>14.6f}")
    print(f"{'Total':<10}{sum(r['counts'].values()):>7}{r['hit_frequency']:>14.6f}{'':>6}{r['rtp']:>14.6f}")
    print()
    print(f"Theoretical RTP:  {r['rtp']:.6f} ({r['rtp'] * 100:.4f}%)")
    print(f"House edge:       {(1 - r['rtp']) * 100:.4f}%")
    print(f"Hit frequency:    {r['hit_frequency']:.6f} ({r['hit_frequency'] * 100:.4f}%)")
    print(f"Std deviation:    {r['sigma']:.4f}")
    print(f"Volatility index: {Z90 * r['sigma']:.4f} (90%), {Z95 * r['sigma']:.4f} (95%)")
    print(f"Max win:          {r['max_win']}x")
    return r


if __name__ == "__main__":
    print_par()
    print()
    print("Balancing example: which '2 Wilds' pay gives exactly 96%?")
    exact = pay_for_target('2 Wilds', 0.96)
    print(f"  exact pay {exact:.4f}; rounded to a whole number of bets: {round(exact)}")
