"""
Fruit Master v1.0 – Monte Carlo simulation
Validates theoretical RTP (96.1125%) and estimates volatility & hit frequency.
"""
import numpy as np

reel1 = np.array(['C','C','C','C','L','L','L','O','O','B','C','C','L','L','O','O','B','W','-','-'])
reel2 = np.array(['C','C','C','L','L','L','O','O','O','B','C','L','L','O','O','B','W','-','-','-'])
reel3 = np.array(['C','C','L','L','L','O','O','O','B','B','C','L','O','O','B','W','-','-','-','-'])

THEORETICAL_RTP = 0.961125
THEORETICAL_HIT = 0.226125


def get_payout(s1, s2, s3):
    """Final balanced paytable – same order as enumeration."""
    symbols = [s1, s2, s3]
    n_wild = symbols.count('W')

    if s1 == 'W' and s2 == 'W' and s3 == 'W':
        return 80
    if all(s in ('B', 'W') for s in symbols):
        return 40
    if all(s in ('O', 'W') for s in symbols):
        return 16
    if all(s in ('L', 'W') for s in symbols):
        return 8
    if all(s in ('C', 'W') for s in symbols):
        return 4
    if n_wild == 2:
        return 10
    if n_wild == 1:
        return 1
    if s1 == 'C' and s2 == 'C':
        return 1
    return 0


def spin():
    return (
        np.random.choice(reel1),
        np.random.choice(reel2),
        np.random.choice(reel3),
    )


def run_simulation(n_spins=1_000_000, seed=42):
    np.random.seed(seed)

    results = np.empty(n_spins, dtype=np.float64)
    for i in range(n_spins):
        results[i] = get_payout(*spin())

    sim_rtp = float(np.mean(results))
    volatility = float(np.std(results))
    hit_freq = float(np.mean(results > 0))
    max_observed = float(np.max(results))

    print("=== Fruit Master v1.0 – Monte Carlo ===")
    print(f"Spins:              {n_spins:,}")
    print(f"Seed:               {seed}")
    print()
    print(f"Simulated RTP:      {sim_rtp:.6f}  ({sim_rtp * 100:.4f}%)")
    print(f"Theoretical RTP:    {THEORETICAL_RTP:.6f}  ({THEORETICAL_RTP * 100:.4f}%)")
    print(f"Difference:         {abs(sim_rtp - THEORETICAL_RTP):.6f}  "
          f"({abs(sim_rtp - THEORETICAL_RTP) * 100:.4f} pp)")
    print()
    print(f"Volatility (std):   {volatility:.6f}")
    print(f"Hit frequency:      {hit_freq:.6f}  ({hit_freq * 100:.4f}%)")
    print(f"Theoretical hit:    {THEORETICAL_HIT:.6f}  ({THEORETICAL_HIT * 100:.4f}%)")
    print(f"Max observed win:   {max_observed:.0f}")
    print()

    # Sanity check
    if abs(sim_rtp - THEORETICAL_RTP) < 0.01:
        print("OK: Simulated RTP is within 1 percentage point of theory.")
    else:
        print("WARN: Larger deviation – check get_payout or increase n_spins.")

    return {
        "n_spins": n_spins,
        "sim_rtp": sim_rtp,
        "theoretical_rtp": THEORETICAL_RTP,
        "volatility": volatility,
        "hit_freq": hit_freq,
        "max_observed": max_observed,
    }


if __name__ == "__main__":
    run_simulation(n_spins=1_000_000, seed=42)