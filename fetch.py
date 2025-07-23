from auth import get_authenticated_session
import requests

def fetch_quote(symbol):
    session = get_authenticated_session()
    url = f"https://api.schwabapi.com/marketdata/v1/quotes/{symbol}"
    response = session.get(url)
    response.raise_for_status()
    return response.json()

def fetch_historical_data(symbol, frequency="daily", period=30):
    session = get_authenticated_session()
    url = f"https://api.schwabapi.com/marketdata/v1/pricehistory"
    params = {
        "symbol": symbol,
        "frequencyType": frequency,
        "period": period
    }
    response = session.get(url, params=params)
    response.raise_for_status()
    return response.json()
def fetch_news(symbol):
    session = get_authenticated_session()
    url = f"https://api.schwabapi.com/marketdata/v1/news/{symbol}"
    response = session.get(url)
    response.raise_for_status()
    return response.json()
def fetch_live_data(symbol):
    session = get_authenticated_session()
    url = f"https://api.schwabapi.com/marketdata/v1/quotes/{symbol}/live"
    response = session.get(url)
    response.raise_for_status()
    return response.json()