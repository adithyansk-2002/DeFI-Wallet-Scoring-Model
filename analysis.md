# Wallet Score Analysis

This document provides an overview of the distribution and behavioral analysis of wallets scored using the Aave V2 credit scoring model.

---

## Score Distribution

Wallets are bucketed into score ranges:

| Score Range | Number of Wallets |
|-------------|-------------------|
| 0–100       | 0                 |
| 100–200     | 0                 |
| 200–300     | 1                 |
| 300–400     | 7                 |
| 400–500     | 187               |
| 500–600     | 1870              |
| 600–700     | 736               |
| 700–800     | 678               |
| 800–900     | 18                |
| 900–1000    | 0                 |

## Behavior by Score Bucket

### Low Scores (0–300)
- High number of `liquidationcall` events
- More `borrow` than `repay`, suggesting risky or abandoned positions
- Low deposit activity, often with minimal amounts
- Possibly bot-like or exploitative behavior

### Mid Scores (400–600)
- Balanced usage, but some inconsistencies in repay-to-borrow or deposit-to-redeem ratios
- Minimal liquidation history
- Average transaction frequency

### High Scores (700–1000)
- Strong repay-to-borrow ratios (>1.0)
- Consistent deposits and healthy redeem patterns
- Very few or no liquidations
- Likely reliable and sophisticated users

---

## Summary

- The scoring model effectively separates high-risk vs. reliable wallet behaviors.
- Scores are interpretable and can be improved with additional time-based or protocol-native metrics.
- Most users fall within the 400–800 score range, indicating relatively moderate usage patterns.