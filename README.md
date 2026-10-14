# Fruit Master – 3-Reel Slot Math Model

Portfolio project: complete math model for a simple 3-reel slot
(exact RTP by enumeration, PAR-style breakdown, paytable balancing, Monte Carlo validation).

## Key results (v1.1)

| Metric | Value |
|--------|--------|
| Theoretical RTP | **95.9875%** |
| Hit frequency | **22.6125%** |
| Standard deviation | **3.814** |
| Volatility index (90%) | **6.27** |
| Max win | **80×** |
| Simulated RTP (1M spins, seed 42) | **96.0006%**, 95% CI [95.25%, 96.75%] |

## What this project includes

- Reel strips and symbol weights
- Paytable with Wild substitution; each spin pays its **highest** qualifying win
- Full enumeration of all 8,000 outcomes: exact RTP, hit frequency, standard deviation, volatility index
- PAR-style table: hits, probability and RTP contribution per category
- Direct balancing: the pay needed for a target RTP is solved, not guessed
- Monte Carlo simulation (1,000,000 spins) checked against the exact values with 95% confidence intervals
- Tests for the evaluation rules and the exact results
- Game math documentation and Excel workbooks

## How to run

```text
pip install -r requirements.txt
python src/enumerate_rtp.py     # exact math and PAR table
python src/simulation.py        # Monte Carlo validation
python -m pytest                # tests (or: python tests/test_model.py)
```

## Project structure

```text
fruit-master-slot-math/
├── README.md
├── requirements.txt
├── src/
│   ├── slot_model.py         # reels, paytable, evaluation (shared)
│   ├── enumerate_rtp.py      # exact math, PAR table, balancing
│   └── simulation.py         # Monte Carlo validation
├── tests/
│   └── test_model.py
├── excel/
│   ├── Fruit_Master.xlsx
│   └── PAR_Sheet_Fruit_Master.xlsx
├── docs/
│   └── game_math_document.md
└── results/
    └── summary.md
```

## Changes in v1.1

- **Highest win is paid.** In v1.0 the rules were checked in a fixed order, so two wilds with a
  cherry paid CCC (4) instead of "2 Wilds" (10), and two wilds with a lemon paid LLL (8): adding a
  symbol could lower the win. 27 of 8,000 outcomes were affected. Now every qualifying win is
  found and the highest is paid.
- **Rebalanced directly.** With the fix the RTP rose to 97.44%. RTP is linear in each pay, so the
  "2 Wilds" pay for 96% was solved directly (6.05) and rounded to 6, giving 95.9875%.
- **Validation by confidence interval** instead of a fixed "within 1 pp" rule.
- One shared model module, a vectorised simulation, exact standard deviation, and tests.
