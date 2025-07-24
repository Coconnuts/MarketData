import pandas as pd
# `analyse.py` - A module for analyzing financial data
def calculate_moving_average(data, window=10):
    df = pd.DataFrame(data)
    df['SMA'] = df['close'].rolling(window=window).mean()
    return df
def detect_trend(data):
    if data['SMA'].iloc[-1] > data['SMA'].iloc[-2]:
        return "uptrend"
    elif data['SMA'].iloc[-1] < data['SMA'].iloc[-2]:
        return "downtrend"
    else:
        return "sideways"
# Calculate Moving Average Difference
def ma_diff(data):
    df = pd.DataFrame(data)
    df['SMA_diff'] = df['SMA'].diff()
    return df
# Calculate Relative Strength Index (RSI) (public code)
def rsi(df, window=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df
# Calculate Bollinger Bands
def bollinger_bands(df, window=20, num_std_dev=2):
    df['SMA'] = df['close'].rolling(window=window).mean()
    df['std_dev'] = df['close'].rolling(window=window).std()
    df['upper_band'] = df['SMA'] + (df['std_dev'] * num_std_dev)
    df['lower_band'] = df['SMA'] - (df['std_dev'] * num_std_dev)
    return df[['close', 'SMA', 'upper_band', 'lower_band']]
# Calculate MACD (Moving Average Convergence Divergence)
def macd(data, short_window=12, long_window=26, signal_window=9):
    df = pd.DataFrame(data)
    df['EMA_short'] = df['close'].ewm(span=short_window, adjust=False).mean()
    df['EMA_long'] = df['close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    df['Signal_line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    return df[['close', 'MACD', 'Signal_line']]
# pct_change function to calculate percentage change
def pct_change(data, periods=1):
    df = pd.DataFrame(data)
    df['pct_change'] = df['close'].pct_change(periods=periods) * 100
    return df[['close', 'pct_change']]
#momentum function to calculate momentum
def momentum(data, window=10):
    df = pd.DataFrame(data)
    df['momentum'] = df['close'].diff(periods=window)
    return df[['close', 'momentum']]
#volatility function to calculate volatility
def volatility(data, window=20):
    df = pd.DataFrame(data)
    df['volatility'] = df['close'].rolling(window=window).std()
    return df[['close', 'volatility']]
# ATR (Average True Range) function to calculate ATR (public code)
def atr(df, window=14):
    df['high_low'] = df['high'] - df['low']
    df['high_close'] = (df['high'] - df['close'].shift()).abs()
    df['low_close'] = (df['low'] - df['close'].shift()).abs()
    df['true_range'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
    df['ATR'] = df['true_range'].rolling(window=window).mean()
    return df[['close', 'ATR']]
# Volume Weighted Average Price (VWAP)
def vwap(data):
    df = pd.DataFrame(data)
    df['cum_volume'] = df['volume'].cumsum()
    df['cum_price_volume'] = (df['close'] * df['volume']).cumsum()
    df['VWAP'] = df['cum_price_volume'] / df['cum_volume']
    return df[['close', 'VWAP']]
# On-Balance Volume (OBV)
def obv(data):
    df = pd.DataFrame(data)
    df['direction'] = df['close'].diff().apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0)
    df['OBV'] = (df['volume'] * df['direction']).cumsum()
    return df[['close', 'OBV']]
# Average Directional Index (ADX)
def adx(data, window=14):
    df = pd.DataFrame(data)
    df['high_diff'] = df['high'].diff()
    df['low_diff'] = df['low'].diff()
    df['tr'] = df[['high_diff', 'low_diff', 'close']].max(axis=1).abs()
    
    df['+DI'] = 100 * (df['high_diff'].clip(lower=0).rolling(window=window).mean() / df['tr'].rolling(window=window).mean())
    df['-DI'] = 100 * (-df['low_diff'].clip(upper=0).rolling(window=window).mean() / df['tr'].rolling(window=window).mean())
    
    df['DX'] = 100 * (abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI']))
    df['ADX'] = df['DX'].rolling(window=window).mean()
    
    return df[['close', '+DI', '-DI', 'ADX']]
#computes features for the prediction model
def compute_features(df):
    df = calculate_moving_average(df)
    df = ma_diff(df)
    df = rsi(df)
    df = bollinger_bands(df)
    df = macd(df)
    df = pct_change(df)
    df = momentum(df)
    df = volatility(df)
    df = atr(df)
    df = vwap(df)
    df = obv(df)
    df = adx(df)

    return df