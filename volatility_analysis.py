import pandas as pd
import os

DATA_DIR = "data/csv/stocks"
volatility_data = []

for file in os.listdir(DATA_DIR):
    df = pd.read_csv(os.path.join(DATA_DIR, file))
    df['Date'] = pd.to_datetime(df['Date'])

    df['Daily Return'] = df['Close'].pct_change()
    volatility = df['Daily Return'].std()

    volatility_data.append({
        "Symbol": file.replace(".csv", ""),
        "Volatility": volatility
    })

vol_df = pd.DataFrame(volatility_data)
vol_df.sort_values("Volatility", ascending=False).head(10)\
      .to_csv("data/csv/top_volatile_stocks.csv", index=False)

print("✅ Volatility analysis completed")
