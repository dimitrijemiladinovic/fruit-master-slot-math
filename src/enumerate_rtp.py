"""
Fruit Master v1.0 – Full enumeration of theoretical RTP
"""
import itertools

reel1 = ['C','C','C','C','L','L','L','O','O','B','C','C','L','L','O','O','B','W','-','-']
reel2 = ['C','C','C','L','L','L','O','O','O','B','C','L','L','O','O','B','W','-','-','-']
reel3 = ['C','C','L','L','L','O','O','O','B','B','C','L','O','O','B','W','-','-','-','-']


def get_payout(s1, s2, s3):
    """Evaluation order: highest priority first. One payout per spin."""
    symbols = [s1, s2, s3]
    n_wild = symbols.count('W')

    # 1. WWW
    if s1 == 'W' and s2 == 'W' and s3 == 'W':
        return 80

    # 2. BBB (B or W)
    if all(s in ('B', 'W') for s in symbols):
        return 40

    # 3. OOO (O or W)
    if all(s in ('O', 'W') for s in symbols):
        return 16

    # 4. LLL (L or W)
    if all(s in ('L', 'W') for s in symbols):
        return 8

    # 5. CCC (C or W)
    if all(s in ('C', 'W') for s in symbols):
        return 4

    # 6. Exactly 2 Wilds
    if n_wild == 2:
        return 10

    # 7. Exactly 1 Wild
    if n_wild == 1:
        return 1

    # 8. CC any
    if s1 == 'C' and s2 == 'C':
        return 1

    # 9. Nothing
    return 0


def enumerate_rtp():
    total = 0
    hit = 0
    n = 0
    payout_counts = {}

    for a, b, c in itertools.product(reel1, reel2, reel3):
        p = get_payout(a, b, c)
        total += p
        n += 1
        if p > 0:
            hit += 1
        payout_counts[p] = payout_counts.get(p, 0) + 1

    rtp = total / n
    hit_freq = hit / n

    print("=== Fruit Master v1.0 – Enumeration ===")
    print("Total outcomes:", n)
    print("Sum of payouts:", total)
    print("Theoretical RTP: {:.6f} ({:.4f}%)".format(rtp, rtp * 100))
    print("House edge: {:.4f}%".format((1 - rtp) * 100))
    print("Hit frequency: {:.6f} ({:.4f}%)".format(hit_freq, hit_freq * 100))
    print("Max win: 80")
    print("Payout distribution:")
    for k in sorted(payout_counts.keys(), reverse=True):
        print(f"  {k}: {payout_counts[k]}")


if __name__ == "__main__":
    enumerate_rtp()