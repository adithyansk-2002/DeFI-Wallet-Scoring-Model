import pandas as pd
import matplotlib.pyplot as plt

scores = pd.read_csv('wallet_scores.csv')
bins = range(0, 1100, 100)
scores['score_range'] = pd.cut(scores['credit_score'], bins=bins)

# Count per bucket
print(scores['score_range'].value_counts().sort_index())

# Plot
scores['credit_score'].hist(bins=20, edgecolor='black')
plt.title('Credit Score Distribution')
plt.xlabel('Score')
plt.ylabel('Number of Wallets')
plt.grid(True)
plt.savefig('data/Figure_1.png')
plt.show()