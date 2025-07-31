from auth import refresh_access_token
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
SAVE_PATH = "data/live/"

# === FUNCTIONS ===

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
    main()
