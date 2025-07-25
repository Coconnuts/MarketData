
import requests
import pandas as pd
import os
from datetime import datetime
import time

# === CONFIG ===
TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "INTC", "CSCO", "PEP",
    "NFLX", "ADBE", "PYPL", "AVGO", "TXN", "QCOM", "COST", "AMAT", "AMD", "INTU",
    "SBUX", "ISRG", "BKNG", "MDLZ", "GILD", "ADI", "LRCX", "FISV", "VRTX", "REGN",
    "MU", "MAR", "KDP", "CTAS", "KLAC", "CDNS", "PANW", "NXPI", "IDXX", "FTNT",
    "EXC", "WBA", "MCHP", "ANSS", "EBAY", "BIIB", "ROST", "PAYX", "ODFL", "VRSK",
    "AEP", "CHTR", "ORLY", "PCAR", "CTSH", "FAST", "WDAY", "SIRI", "XEL", "DLTR",
    "ALGN", "TEAM", "ZS", "MDB", "DDOG", "DOCU", "SNOW", "OKTA", "CRWD", "NET",
    "PLTR", "ABNB", "UBER", "LYFT", "SHOP", "SQ", "ROKU", "ZM", "BIDU", "NTES",
    "JD", "PDD", "BABA", "TSM", "ASML", "ARM", "ON", "MRVL", "SWKS", "TTD", "TTWO",
    "EA", "ATVI", "FSLY", "RBLX", "COIN", "HUBS", "FVRR", "DOCN", "TWLO", "DUOL"
]

# Replace with your actual token from Schwab or mock data
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
SAVE_PATH = "data/live/live_prices.csv"

# === FUNCTIONS ===

def fetch_ticker_data(ticker):
    url = f"https://api.schwabapi.com/market/quote/{ticker}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get(ticker)
    return None

def get_formatted_row(ticker_data, ticker):
    now = datetime.now().strftime("%Y-%m-%d")
    return {
        "Date": now,
        "Ticker": ticker,
        "Close/Last": ticker_data.get("lastPrice"),
        "Open": ticker_data.get("openPrice"),
        "High": ticker_data.get("highPrice"),
        "Low": ticker_data.get("lowPrice"),
        "Volume": ticker_data.get("totalVolume"),
    }

def save_to_csv(rows):
    df = pd.DataFrame(rows)
    file_exists = os.path.exists(SAVE_PATH)

    if file_exists:
        df.to_csv(SAVE_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(SAVE_PATH, index=False)

def main():
    all_rows = []
    for ticker in TICKERS:
        data = fetch_ticker_data(ticker)
        if data:
            row = get_formatted_row(data, ticker)
            all_rows.append(row)
        time.sleep(0.1)  # avoid rate limit
    if all_rows:
        save_to_csv(all_rows)
        print(f"✅ Appended {len(all_rows)} rows to {SAVE_PATH}")
    else:
        print("⚠️ No data fetched.")

if __name__ == "__main__":
    main()
