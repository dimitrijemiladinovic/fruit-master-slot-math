# Fruit Master – 3-Reel Slot Math Model

Portfolio project: complete math model for a simple 3-reel slot
(theoretical RTP, paytable balancing, Monte Carlo validation).

## Key results

| Metric | Value |
|--------|--------|
| Theoretical RTP | **96.11%** |
| Simulated RTP (1M spins) | **96.64%** |
| Hit frequency | **22.61%** |
| Volatility (std) | **3.82** |
| Max win | **80×** |

## What this project includes

- Reel strips and symbol weights
- Paytable with Wild substitution and strict evaluation order
- Full enumeration of all 8,000 outcomes (exact theoretical RTP)
- Iterative paytable balancing (132% → 96%)
- Monte Carlo simulation (1,000,000 spins)
- Game math documentation and PAR-style summary

## Project structure

```text
fruit-master-slot-math/
├── README.md
├── excel/
│   ├── Fruit_Master.xlsx
│   └── PAR_Sheet_Fruit_Master.xlsx
├── src/
│   ├── enumerate_rtp.py
│   └── simulation.py
├── docs/
│   └── game_math_document.md
└── results/
    └── summary.md