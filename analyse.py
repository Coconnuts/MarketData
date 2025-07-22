import pandas as pd

def calculate_moving_average(data, window=10):
    df = pd.DataFrame(data)
    df['SMA'] = df['close'].rolling(window=window).mean()
    return df
def detect_trend(data):
    if data['SMA'].iloc[-1] > data['SMA'].iloc[-2]:
        return "uptrend"
    elif data['SMA'].iloc[-1] > data['SMA'].iloc[-2]:
        return "downtrend"
    else:
        return "sideways"
    
def ma_difference(data):
    df = pd.DataFrame(data)
    df['SMA_diff'] = df['SMA'].diff()
    return df