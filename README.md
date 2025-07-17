# Aave Credit Scoring Engine

This project assigns a **credit score (0–1000)** to wallets based on historical transaction data from the Aave V2 protocol. Higher scores indicate responsible and reliable user behavior; lower scores highlight riskier or exploitative patterns.

---

## Project Structure

```
aave-credit-score/
│
├── score_generator.py       # Main scoring script
├── README.md                # Project overview
├── analysis.md              # Score analysis & distribution
├── requirements.txt         # Python dependencies
└── data/
    └── user-wallet-transactions.json  # Input transaction data
```

---

## How It Works

### 1. **Feature Engineering**

For each wallet, we compute:

- Total and count of:
  - Deposits
  - Borrows
  - Repays
  - Redeems
  - Liquidations
- Ratios:
  - Repay-to-Borrow Ratio
  - Deposit-to-Redeem Ratio
- Unique assets interacted with
- Total transaction count

### 2. **Scoring Logic**

Wallets are scored using a heuristic model:

- Starts at **500 base points**
- Rewards:
  - High repay/borrow ratio (+ up to 200)
  - High deposit/redeem ratio (+ up to 100)
  - Large deposits (+ up to 100)
- Penalties:
  - Frequent liquidations (- up to 200)
  - High un-repaid borrowing (-50)

The final score is clipped between 0 and 1000.

---

## Setup & Run

### Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

### Generate Scores

```bash
python score_generator.py --input data/user-wallet-transactions.json --output wallet_scores.csv
```

---

## Output

- `wallet_scores.csv` – contains two columns:
  - `wallet`: wallet address
  - `credit_score`: score between 0 and 1000

---

## Notes

- No on-chain labels are used — scores are purely behavior-based.
- The scoring logic is interpretable and easy to modify.

---

## Extensibility

To improve the scoring model:

- Use time-based features (e.g., recency, streaks)
- Include protocol-native parameters (e.g., LTV, health factor)
- Train a supervised ML model with labeled default/bot accounts

