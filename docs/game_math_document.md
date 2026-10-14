# Fruit Master – Game Math Document

**Version:** 1.1  
**Game type:** 3-reel, 1-line slot  
**Bet:** 1 credit per spin  
**Total outcomes:** 20 × 20 × 20 = 8,000  
**Date:** 2026-10-14

---

## 1. Game overview

Fruit Master is a portfolio 3-reel slot math model built to demonstrate an
end-to-end game mathematics workflow:

- reel strip design and symbol weights
- paytable with Wild substitution
- one payout per spin: the highest qualifying win
- exact theoretical RTP, hit frequency and standard deviation via full enumeration
- PAR-style breakdown of RTP contributions
- balancing a pay to a target RTP by direct calculation
- Monte Carlo validation (1,000,000 spins) with confidence intervals

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
| C (cherry) | 6 | 4 | 3 |
| L (lemon) | 5 | 5 | 4 |
| O (orange) | 4 | 5 | 5 |
| B (bar) | 2 | 2 | 3 |
| W (wild) | 1 | 1 | 1 |
| - (blank) | 2 | 3 | 4 |
| **Total** | **20** | **20** | **20** |

Each reel stop is equally likely and the reels are independent.

---

## 3. Paytable (v1.1)

| Combination | Payout | Rule |
|-------------|--------|------|
| W W W | 80 | Three wilds |
| B B B | 40 | Each reel B or W |
| O O O | 16 | Each reel O or W |
| L L L | 8 | Each reel L or W |
| Exactly 2 Wilds | 6 | Any third symbol |
| C C C | 4 | Each reel C or W |
| Exactly 1 Wild | 1 | Anywhere on the line |
| C C any | 1 | Reel 1 = C and reel 2 = C |
| Other | 0 | — |

**Evaluation:** every combination the outcome qualifies for is found, and only
the highest pay is awarded. Example: W W C qualifies for C C C (4) and
"Exactly 2 Wilds" (6), and pays 6. W W L qualifies for L L L (8) and
"Exactly 2 Wilds" (6), and pays 8.

**Max win:** 80× bet

---

## 4. Exact results (full enumeration)

| Category | Hits | Probability | Pay | RTP contribution |
|----------|-----:|------------:|----:|-----------------:|
| W W W | 1 | 0.000125 | 80 | 0.010000 |
| B B B | 35 | 0.004375 | 40 | 0.175000 |
| O O O | 179 | 0.022375 | 16 | 0.358000 |
| L L L | 179 | 0.022375 | 8 | 0.179000 |
| Exactly 2 Wilds | 22 | 0.002750 | 6 | 0.016500 |
| C C C | 126 | 0.015750 | 4 | 0.063000 |
| Exactly 1 Wild | 883 | 0.110375 | 1 | 0.110375 |
| C C any | 384 | 0.048000 | 1 | 0.048000 |
| **Total** | **1,809** | **0.226125** | | **0.959875** |

| Metric | Value |
|--------|-------|
| **Theoretical RTP** | **95.9875%** |
| House edge | 4.0125% |
| **Hit frequency** | **22.6125%** (about 1 spin in 4.4) |
| Standard deviation σ | 3.8142 |
| Volatility index (90%, z = 1.645) | 6.27 |
| Volatility index (95%, z = 1.96) | 7.48 |
| Max win | 80× |

Formulas, with outcome probabilities pₖ and pays wₖ:

- RTP = Σ pₖ wₖ
- Hit frequency = Σ pₖ over outcomes with wₖ > 0
- σ² = Σ pₖ wₖ² − RTP²
- After n spins the actual RTP lies in RTP ± z·σ/√n with the chosen confidence.
  For 1,000,000 spins at 95%: ±1.96 × 3.814 / 1000 = ±0.75 percentage points.

---

## 5. Balancing

RTP is linear in each pay as long as the same outcomes are paid as that
category: raising a pay by one unit adds (hits / 8,000) to the RTP. So the pay
for a target RTP can be solved directly:

new pay = old pay + (target RTP − current RTP) × 8,000 / hits

Because only the highest win is paid, a pay change can move outcomes between
categories (for example, once "2 Wilds" pays less than 8, W W L is paid as
L L L). `pay_for_target()` in `src/enumerate_rtp.py` therefore repeats the
linear step until the category counts stop changing.

| Version | RTP | Note |
|---------|-----|------|
| v1.0, early drafts | 132.30% → 66.74% → 109.71% | Paytable tuned by trial and error |
| v1.0 final | 96.1125% | Fixed priority order, 2 Wilds = 10 |
| v1.1 rule fix only | 97.4375% | Highest win paid, 2 Wilds = 10 |
| **v1.1 final** | **95.9875%** | 2 Wilds solved for 96% (6.05), rounded to 6 |

### What changed from v1.0 and why

In v1.0 the combinations were checked in a fixed order and the first match was
paid. C C C and L L L were checked before "Exactly 2 Wilds", so W W C paid 4
and W W L paid 8, while W W blank paid 10: adding a symbol could lower the
win, which players would see as an error. This affected 27 of the 8,000
outcomes (+1.325 percentage points of RTP once fixed). v1.1 pays the highest
qualifying win, and a test checks that turning a blank into any symbol never
lowers the pay.

---

## 6. Monte Carlo validation

- Spins: 1,000,000, seed 42 (NumPy `default_rng`)
- Same evaluation as the enumeration (`src/slot_model.py`); reel stops drawn
  uniformly and independently

| Metric | Simulated | 95% interval | Exact | Result |
|--------|-----------|--------------|-------|--------|
| RTP | 96.0006% | 95.2548% – 96.7464% | 95.9875% | inside |
| Hit frequency | 22.6340% | 22.5520% – 22.7160% | 22.6125% | inside |
| Standard deviation | 3.8049 | | 3.8142 | |
| Max observed win | 80× | | 80× | |

The model is accepted when the exact values lie inside the simulation
intervals. A 95% interval misses the true value in about 1 run in 20, so a
single miss with another seed is not by itself a sign of an error; a
repeated miss is.

---

## 7. Assumptions

- Single payline; bet = 1
- Wild substitutes for C, L, O, B
- One payout per spin: the highest qualifying win
- Independent uniform reel stops
- No free spins / bonus feature in this version

---

## 8. Files

| Path | Description |
|------|-------------|
| `src/slot_model.py` | Reels, paytable and evaluation, shared by all scripts |
| `src/enumerate_rtp.py` | Full enumeration, PAR table, balancing |
| `src/simulation.py` | Monte Carlo validation with confidence intervals |
| `tests/test_model.py` | Rule and result checks |
| `excel/Fruit_Master.xlsx` | Reel strips, counts, paytable, combinations, summary |
| `excel/PAR_Sheet_Fruit_Master.xlsx` | PAR-style one-page summary |
| `results/summary.md` | Simulation summary |
