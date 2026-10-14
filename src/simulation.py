"""
Fruit Master v1.1 - Monte Carlo validation of the theoretical math.

Uses the same game model as the enumeration (slot_model.py). Reel stops are
drawn uniformly and independently; the RTP and hit frequency are reported with
95% confidence intervals, and the model counts as validated when the exact
values lie inside those intervals.
"""
import numpy as np

from slot_model import REELS, enumerate_cycle, payout_table

Z95 = 1.96


def run_simulation(n_spins=1_000_000, seed=42):
    rng = np.random.default_rng(seed)
    pays = np.array(payout_table(), dtype=np.float64)          # shape (20, 20, 20)
    stops = [rng.integers(0, len(reel), size=n_spins) for reel in REELS]
    wins = pays[stops[0], stops[1], stops[2]]

    mean = wins.mean()
    sd = wins.std(ddof=1)
    half = Z95 * sd / np.sqrt(n_spins)
    hit = (wins > 0).mean()
    hit_half = Z95 * np.sqrt(hit * (1 - hit) / n_spins)

    exact = enumerate_cycle()
    rtp_ok = mean - half <= exact['rtp'] <= mean + half
    hit_ok = hit - hit_half <= exact['hit_frequency'] <= hit + hit_half

    print("=== Fruit Master v1.1 - Monte Carlo ===")
    print(f"Spins: {n_spins:,}   seed: {seed}")
    print()
    print(f"Simulated RTP:   {mean * 100:.4f}%  95% CI [{(mean - half) * 100:.4f}%, {(mean + half) * 100:.4f}%]")
    print(f"Theoretical RTP: {exact['rtp'] * 100:.4f}%  -> {'inside' if rtp_ok else 'OUTSIDE'} the interval")
    print(f"Simulated hit:   {hit * 100:.4f}%  95% CI [{(hit - hit_half) * 100:.4f}%, {(hit + hit_half) * 100:.4f}%]")
    print(f"Theoretical hit: {exact['hit_frequency'] * 100:.4f}%  -> {'inside' if hit_ok else 'OUTSIDE'} the interval")
    print(f"Std deviation:   {sd:.4f} (exact {exact['sigma']:.4f})")
    print(f"Max observed:    {wins.max():.0f}x")
    print()
    print("Validated." if rtp_ok and hit_ok else
          "Not validated: check the model, or remember that 1 run in 20 falls outside a 95% interval.")

    return {
        'n_spins': n_spins, 'seed': seed, 'sim_rtp': float(mean), 'ci_half_width': float(half),
        'sim_hit': float(hit), 'sd': float(sd), 'max_observed': float(wins.max()),
        'rtp_ok': bool(rtp_ok), 'hit_ok': bool(hit_ok),
    }


if __name__ == "__main__":
    run_simulation()
