import pandas as pd
import os

INPUT_FILE = "data/csv/all_stocks.csv"
OUTPUT_DIR = "data/csv/stocks"

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

df['Date'] = pd.to_datetime(df['Date'])

for symbol, group in df.groupby("Symbol"):
    symbol_file = os.path.join(OUTPUT_DIR, f"{symbol}.csv")
    group.sort_values("Date").to_csv(symbol_file, index=False)

print(f"✅ Created {df['Symbol'].nunique()} stock CSV files")
