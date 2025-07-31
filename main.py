from fetch import fetch_historical_data
from analyse import calculate_moving_average, detect_trend
from strategy import generate_signal

def run(symbol):
    print(f"Running strategy for {symbol}...")
    data = fetch_historical_data(symbol)['candels']
    df = calculate_moving_average(data)
    # Assuming you want to detect trend on the latest row
    trend = detect_trend(df.iloc[-1])
    signal = generate_signal(trend)
    print(f"Trend: {trend} -> Signal: {signal}")

if __name__ == "__main__":
    run("AAPL") # example