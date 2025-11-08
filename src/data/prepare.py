# src/data/prepare.py
import pandas as pd
from sklearn.model_selection import train_test_split
import os

def prepare_data(output_dir="data/processed", csv_path="data/raw/financial_phrasebank.csv"):
    df = pd.read_csv(csv_path)
    df.rename(columns={"Sentence": "text", "Sentiment": "label"}, inplace=True)
    label_map = {
        "negative": "Bearish",
        "neutral": "Neutral",
        "positive": "Bullish"
    }
    df["label_name"] = df["label"].map(label_map)
    df["text"] = df["text"].str.strip().str.replace(r"\s+", " ", regex=True)

    # Train/test split
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["label"])

    # Ensure output folder exists
    os.makedirs(output_dir, exist_ok=True)

    # Save CSVs
    train_df.to_csv(os.path.join(output_dir, "train.csv"), index=False)
    test_df.to_csv(os.path.join(output_dir, "test.csv"), index=False)
    df.to_csv(os.path.join(output_dir, "full.csv"), index=False)

    print(f"Data prepared: {len(train_df)} train / {len(test_df)} test")

if __name__ == "__main__":
    prepare_data()
