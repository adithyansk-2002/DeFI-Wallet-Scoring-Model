import json
import pandas as pd
import numpy as np
from collections import defaultdict
import argparse

# Scoring bounds
MAX_SCORE = 1000
MIN_SCORE = 0


def load_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)


def preprocess(df):
    df['wallet'] = df['userWallet']
    df['action'] = df['action'].str.lower()
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['amountUSD'] = df['actionData'].apply(lambda x: float(x.get('amount', 0)) * float(x.get('assetPriceUSD', 0)))
    return df


def extract_features(df):
    grouped = df.groupby('wallet')
    features = []

    for wallet, group in grouped:
        f = {'wallet': wallet}
        for action in ['deposit', 'borrow', 'repay', 'redeemunderlying', 'liquidationcall']:
            action_df = group[group['action'] == action]
            f[f'{action}_count'] = len(action_df)
            f[f'{action}_amount_usd'] = action_df['amountUSD'].sum()

        # Ratios and derived features
        f['repay_to_borrow_ratio'] = (
            f['repay_amount_usd'] / f['borrow_amount_usd'] if f['borrow_amount_usd'] > 0 else 0
        )
        f['deposit_to_redeem_ratio'] = (
            f['deposit_amount_usd'] / f['redeemunderlying_amount_usd'] if f['redeemunderlying_amount_usd'] > 0 else 0
        )
        f['total_txn_count'] = len(group)
        f['unique_assets'] = group['actionData'].apply(lambda x: x.get('assetSymbol')).nunique()

        features.append(f)

    return pd.DataFrame(features)


def score_wallets(df):
    scores = []
    for _, row in df.iterrows():
        score = 500  # Base score

        # Positive factors
        score += min(row['repay_to_borrow_ratio'] * 100, 200)
        score += min(row['deposit_to_redeem_ratio'] * 20, 100)
        score += min(row['deposit_amount_usd'] / 5000, 100)

        # Negative factors
        score -= min(row['liquidationcall_count'] * 50, 200)
        score -= 50 if row['borrow_amount_usd'] > row['repay_amount_usd'] * 1.5 else 0

        # Normalize
        score = max(MIN_SCORE, min(MAX_SCORE, int(score)))
        scores.append(score)

    df['credit_score'] = scores
    return df


def main(input_path, output_path):
    df_raw = load_data(input_path)
    df_processed = preprocess(df_raw)
    df_features = extract_features(df_processed)
    df_scored = score_wallets(df_features)

    df_scored[['wallet', 'credit_score']].to_csv(output_path, index=False)
    print(f"Wallet scores saved to {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/user-wallet-transactions.json')
    parser.add_argument('--output', default='wallet_scores.csv')
    args = parser.parse_args()

    main(args.input, args.output)