import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ================================
# CONFIG
# ================================
st.set_page_config(
    page_title="Stock Performance Dashboard",
    layout="wide"
)

DATA_PATH = "data/csv/all_stocks.csv"

# ================================
# LOAD DATA
# ================================
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    # Standardize column names
    if 'Symbol' in df.columns:
        df.rename(columns={'Symbol': 'Ticker'}, inplace=True)

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(['Ticker', 'Date'])
    return df

df = load_data()

# ================================
# TITLE
# ================================
st.title("📈 Stock Performance Dashboard")

# ================================
# MARKET OVERVIEW
# ================================
st.subheader("📊 Market Overview")

yearly_returns = (
    df.groupby('Ticker')
      .apply(lambda x: (x.iloc[-1]['Close'] - x.iloc[0]['Close']) / x.iloc[0]['Close'])
      .reset_index(name='Yearly Return')
)

green = (yearly_returns['Yearly Return'] > 0).sum()
red = (yearly_returns['Yearly Return'] <= 0).sum()

avg_price = df['Close'].mean()
avg_volume = df['Volume'].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("🟢 Green Stocks", green)
c2.metric("🔴 Red Stocks", red)
c3.metric("📈 Avg Price", f"{avg_price:.2f}")
c4.metric("📊 Avg Volume", f"{int(avg_volume):,}")

# ================================
# SIDEBAR
# ================================
st.sidebar.title("Stock Selection")
stocks = sorted(df['Ticker'].dropna().unique())
selected_stock = st.sidebar.selectbox("Select a Stock", stocks)

stock_df = df[df['Ticker'] == selected_stock]

# ================================
# STOCK DATA TABLE
# ================================
st.subheader(f"📄 {selected_stock} – Recent Data")
st.dataframe(stock_df.tail(20), use_container_width=True)

# ================================
# CLOSING PRICE TREND
# ================================
st.subheader("📉 Closing Price Over Time")

fig, ax = plt.subplots()
ax.plot(stock_df['Date'], stock_df['Close'])
ax.set_xlabel("Date")
ax.set_ylabel("Close Price")
st.pyplot(fig)

# ================================
# TOP GAINERS & LOSERS (YEARLY)
# ================================
st.subheader("🟢🔴 Top 10 Gainers & Losers (Yearly)")

yearly = df.groupby('Ticker').agg(
    first_close=('Close', 'first'),
    last_close=('Close', 'last')
)

yearly['Return %'] = (
    (yearly['last_close'] - yearly['first_close']) / yearly['first_close']
) * 100

yearly = yearly.dropna()

top_gainers = yearly.sort_values('Return %', ascending=False).head(10)
top_losers = yearly.sort_values('Return %').head(10)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🟢 Top 10 Gainers")
    st.bar_chart(top_gainers['Return %'])

with col2:
    st.markdown("### 🔴 Top 10 Losers")
    st.bar_chart(top_losers['Return %'])

# ================================
# VOLATILITY ANALYSIS
# ================================
st.subheader("⚡ Top 10 Most Volatile Stocks")

df['Daily Return'] = df.groupby('Ticker')['Close'].pct_change()

volatility = df.groupby('Ticker')['Daily Return'].std().dropna()
top_volatility = volatility.sort_values(ascending=False).head(10)

st.bar_chart(top_volatility)

# ================================
# CUMULATIVE RETURN (TOP 5)
# ================================
st.subheader("📈 Cumulative Return (Top 5 Stocks)")

cum_df = df.sort_values(['Ticker', 'Date']).copy()

cum_df['Daily Return'] = cum_df.groupby('Ticker')['Close'].pct_change()

cum_df['Cumulative Return'] = (
    cum_df.groupby('Ticker')['Daily Return']
          .transform(lambda x: (1 + x).cumprod() - 1)
)

top5 = (
    cum_df.groupby('Ticker')['Cumulative Return']
          .last()
          .sort_values(ascending=False)
          .head(5)
          .index
)

plot_df = cum_df[cum_df['Ticker'].isin(top5)]

st.line_chart(
    plot_df.pivot(index='Date', columns='Ticker', values='Cumulative Return')
)

# ================================
# STOCK PRICE CORRELATION
# ================================
st.subheader("🔗 Stock Price Correlation")

pivot_close = df.pivot(index='Date', columns='Ticker', values='Close')
corr = pivot_close.corr()

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, cmap="coolwarm")
st.pyplot(fig)
