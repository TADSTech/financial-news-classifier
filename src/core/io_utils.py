import pandas as pd
import os

def load_file(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(path)
        # try auto-detect text column
        text_col = df.columns[0]
        return df[text_col].dropna().tolist()
    elif ext in [".txt", ".md"]:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    else:
        raise ValueError("Unsupported file format (use CSV or TXT)")
