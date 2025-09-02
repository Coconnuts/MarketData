from auth import refresh_access_token
import requests
import pandas as pd
import os
import pytz
from datetime import datetime, time as dtime
import time
# === CONFIG ===
TICKERS = [
    "AAPL", "ABNB", "ADBE", "ADI", "AEP", "ALGN", "AMD", "AMAT", "AMZN", "ANSS",
    "ARM", "ASML", "ATVI", "AVGO", "BABA", "BIDU", "BIIB", "BKNG", "CDNS", "CHTR",
    "COIN", "COST", "CRWD", "CSCO", "CTAS", "CTSH", "DDOG", "DLTR", "DOCN", "DOCU",
    "DUOL", "EA", "EBAY", "EXC", "FAST", "FISV", "FSLY", "FTNT", "FVRR", "GILD",
    "GOOGL", "HUBS", "IDXX", "INTC", "INTU", "ISRG", "JD", "KDP", "KLAC", "LRCX",
    "LYFT", "MAR", "MDB", "MCHP", "MDLZ", "META", "MRVL", "MSFT", "MU", "NET",
    "NFLX", "NTES", "NVDA", "NXPI", "ODFL", "OKTA", "ON", "ORLY", "PANW", "PDD",
    "PAYX", "PCAR", "PEP", "PLTR", "PYPL", "QCOM", "RBLX", "REGN", "ROKU", "ROST",
    "SBUX", "SHOP", "SIRI", "SNOW", "SQ", "SWKS", "TEAM", "TSM", "TSLA", "TTD",
    "TTWO", "TWLO", "UBER", "VRSK", "VRTX", "WBA", "WDAY", "XEL", "ZM", "ZS"
]

# Replace with your actual token from Schwab or mock data
SAVE_PATH = "data/live/"

# === FUNCTIONS ===

def is_market_open():
    est = pytz.timezone('US/Eastern')
    now = datetime.now(est)
    market_open = dtime(9, 30)
    market_close = dtime(16, 0)
    return market_open <= now.time() <= market_close and now.weekday() < 5

def fetch_ticker_data(tickers, access_token):
    url = "https://api.schwabapi.com/marketdata/v1/quotes"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"symbols": ",".join(tickers)}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to fetch quotes: {response.status_code}")
        print(response.text)
        return None

def get_formatted_row(ticker_data, ticker):
    quote = ticker_data.get("quote", {})
    now = datetime.now().strftime("%Y-%m-%d")
    return {
        "Date": now,
        "Ticker": ticker,
        "Close/Last": quote.get("lastPrice"),
        "Open": quote.get("openPrice"),
        "High": quote.get("highPrice"),
        "Low": quote.get("lowPrice"),
        "Volume": quote.get("totalVolume"),
    }

def save_to_csv(rows):
    os.makedirs(SAVE_PATH, exist_ok=True)
    for row in rows:
        df = pd.DataFrame([row])
        filename = os.path.join(SAVE_PATH, f"{row['Ticker']}.csv")
        file_exists = os.path.exists(filename)
        df.to_csv(filename, mode='a', header=not file_exists, index=False)

def main():
    access_token = refresh_access_token()
    if not access_token:
        print("❌ Could not refresh token.")
        return

    all_rows = []
    batch_size = 25

    for i in range(0, len(TICKERS), batch_size):
        batch = TICKERS[i:i + batch_size]
        quote_data = fetch_ticker_data(batch, access_token)  # ✅ define it here
        if quote_data:
            print("🔎 Sample response keys:", list(quote_data.keys()))  # 🧪 inspect this
            for ticker, data in quote_data.items():
                row = get_formatted_row(data, ticker)
                all_rows.append(row)
        time.sleep(0.2)
    if all_rows:
        save_to_csv(all_rows)
        print(f"✅ Appended {len(all_rows)} rows to {SAVE_PATH}")
    else:
        print("⚠️ No data fetched.")

if __name__ == "__main__":
    while True:
        if is_market_open():
            print("📈 Market is open. Waiting 1 hour...")
            main()
        else:
            print("Market closed. Waiting...")
        time.sleep(3600)