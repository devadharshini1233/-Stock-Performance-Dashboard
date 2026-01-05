import pandas as pd
import os

DATA_DIR = "data/csv/stocks"

results = []

for file in os.listdir(DATA_DIR):
    df = pd.read_csv(os.path.join(DATA_DIR, file))
    df['Date'] = pd.to_datetime(df['Date'])

    start_price = df.iloc[0]['Close']
    end_price = df.iloc[-1]['Close']

    yearly_return = ((end_price - start_price) / start_price) * 100

    results.append({
        "Symbol": file.replace(".csv", ""),
        "Yearly Return (%)": yearly_return,
        "Average Price": df['Close'].mean(),
        "Average Volume": df['Volume'].mean()
    })

summary_df = pd.DataFrame(results)

summary_df.to_csv("data/csv/market_summary.csv", index=False)
print("✅ Market summary created")
