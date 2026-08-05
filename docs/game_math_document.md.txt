# Fruit Master – Game Math Document

**Version:** 1.0 (balanced)  
**Game type:** 3-reel, 1-line slot  
**Bet:** 1 credit per spin  
**Total outcomes:** 20 × 20 × 20 = 8,000  
**Date:** 2026-08-05

---

## 1. Game overview

Fruit Master is a portfolio 3-reel slot math model built to demonstrate
end-to-end game mathematics workflow:

- reel strip design and symbol weights
- paytable with Wild substitution
- strict evaluation order (one payout per spin)
- exact theoretical RTP via full enumeration
- iterative paytable balancing to a commercial target (~96%)
- Monte Carlo validation (1,000,000 spins)
- volatility and hit frequency

---

## 2. Reel strips (20 positions each)

**Reel 1:**  
C, C, C, C, L, L, L, O, O, B, C, C, L, L, O, O, B, W, -, -

**Reel 2:**  
C, C, C, L, L, L, O, O, O, B, C, L, L, O, O, B, W, -, -, -

**Reel 3:**  
C, C, L, L, L, O, O, O, B, B, C, L, O, O, B, W, -, -, -, -

### Symbol counts

| Symbol | Reel 1 | Reel 2 | Reel 3 |
|--------|--------|--------|--------|
| C | 6 | 4 | 3 |
| L | 5 | 5 | 4 |
| O | 4 | 5 | 5 |
| B | 2 | 2 | 3 |
| W | 1 | 1 | 1 |
| - | 2 | 3 | 4 |
| **Total** | **20** | **20** | **20** |

Each reel stop is equally likely.

---

## 3. Final paytable (v1.0)

| Combination | Payout | Notes |
|-------------|--------|--------|
| W W W | 80 | Three Wilds |
| B B B | 40 | Wild may substitute for B |
| O O O | 16 | Wild may substitute for O |
| L L L | 8 | Wild may substitute for L |
| C C C | 4 | Wild may substitute for C |
| Exactly 2 Wilds | 10 | If not already paid as a higher triple |
| Exactly 1 Wild | 1 | If not already paid as a higher triple |
| C C any | 1 | Reel1=C, Reel2=C; if not paid higher |
| Other | 0 | — |

**Max win:** 80× bet

---

## 4. Evaluation order

Each spin receives exactly one payout (first match wins):

1. WWW → 80  
2. BBB (each reel is B or W) → 40  
3. OOO (each reel is O or W) → 16  
4. LLL (each reel is L or W) → 8  
5. CCC (each reel is C or W) → 4  
6. Exactly 2 Wilds → 10  
7. Exactly 1 Wild → 1  
8. CC any → 1  
9. 0  

---

## 5. Methodology

### 5.1 Theoretical RTP

Full enumeration of all 8,000 outcomes. For every index triple `(i, j, k)`,
symbols are read from the three reels and passed to `get_payout()`.

RTP = (sum of all payouts) / 8000

### 5.2 Balancing history

| Stage | RTP | Action |
|-------|-----|--------|
| Initial paytable | 132.30% | Over-paying |
| Strong reduction | 66.74% | Too low |
| Intermediate | 109.71% | Still high |
| **Final v1.0** | **96.11%** | Target ~94–97% |

Reel strips and evaluation order were kept fixed; only paytable values changed.

### 5.3 Monte Carlo validation

- Spins: 1,000,000  
- Seed: 42  
- Same `get_payout()` as enumeration  

---

## 6. Results

### Theoretical (enumeration)

| Metric | Value |
|--------|--------|
| Sum of payouts | 7,689 |
| **Theoretical RTP** | **96.1125%** |
| House edge | 3.8875% |
| **Hit frequency** | **22.6125%** |
| Max win | 80× |

### Payout distribution (enumeration)

| Payout | Count |
|--------|------:|
| 80 | 1 |
| 40 | 35 |
| 16 | 179 |
| 10 | 9 |
| 8 | 179 |
| 4 | 139 |
| 1 | 1,267 |
| 0 | 6,191 |

### Simulation (1,000,000 spins, seed 42)

| Metric | Value |
|--------|--------|
| **Simulated RTP** | **96.6397%** |
| Difference vs theory | 0.5272 percentage points |
| **Volatility (std)** | **3.8224** |
| Hit frequency (sim) | 22.6385% |
| Max observed win | 80 |

Simulated RTP is within 1 pp of theory → model validated.

---

## 7. Assumptions

- Single payline; bet = 1  
- Wild substitutes for C, L, O, B  
- Strict priority order (no double counting)  
- Independent uniform reel stops  
- No free spins / bonus feature in this version  

---

## 8. Files

| Path | Description |
|------|-------------|
| `excel/Fruit_Master.xlsx` | Reel strips, counts, Summary |
| `excel/PAR_Sheet_Fruit_Master.xlsx` | PAR-style one-page summary |
| `src/enumerate_rtp.py` | Full enumeration |
| `src/simulation.py` | Monte Carlo 1M spins |
| `docs/game_math_document.md` | This document |
| `results/summary.md` | Simulation summary |

---

## 9. Conclusion

Fruit Master demonstrates a complete junior-level game math workflow:
design → exact RTP → balancing → simulation → documentation.
Final theoretical RTP is **96.11%**, validated by Monte Carlo at **96.64%**.