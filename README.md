# -Stock-Performance-Dashboard
The Stock Performance Dashboard aims to provide a comprehensive visualization and analysis of the Nifty 50 stocks' performance over the past year. The project will analyze daily stock data, including open, close, high, low, and volume values. 

# 📈 Data-Driven Stock Analysis Dashboard

## Project Overview
This project analyzes Nifty 50 stock performance over the past year using Python, Pandas, SQL concepts, and visualization tools like Streamlit and Power BI.

The dashboard helps investors and analysts understand:
- Top gainers and losers
- Market overview
- Volatility and risk
- Cumulative stock performance
- Stock price correlations

## Tech Stack
- Python
- Pandas
- Streamlit
- Matplotlib & Seaborn
- SQL (MySQL/PostgreSQL)
- Power BI

## Project Workflow
1. Raw stock data provided in YAML format
2. YAML files converted to CSV
3. Data cleaned and transformed using Pandas
4. Key metrics calculated:
   - Yearly returns
   - Volatility
   - Cumulative returns
5. Interactive dashboard built using Streamlit

## How to Run the Project
```bash
pip install -r requirements.txt
streamlit run streamlit_app/app.py
