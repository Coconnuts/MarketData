import pandas as pd
# `analyse.py` - A module for analyzing financial data
def calculate_moving_average(df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    df['SMA'] = df['close'].rolling(window=window).mean()
    return df
def detect_trend(row: pd.Series) -> str:
    if pd.isna(row['SMA']) or pd.isna(row['prev_SMA']):
        return "sideways"
    if row['SMA'] > row['prev_SMA']:
        return "uptrend"
    elif row['SMA'] < row['prev_SMA']:
        return "downtrend"
    else:
        return "sideways"
def ma_diff(df: pd.DataFrame) -> pd.DataFrame:
    if 'SMA' not in df:
        df = calculate_moving_average(df)
    df['SMA_diff'] = df['SMA'].diff()
    return df
def rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    df_numeric = pd.to_numeric(df['close'], errors='coerce')
    delta = df_numeric.diff().astype(float)
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['RSI'] = df['RSI'].fillna(0)  # Optional: fill initial NaNs with 0
    return df
def bollinger_bands(df: pd.DataFrame, window: int = 20, num_std_dev: int = 2) -> pd.DataFrame:
    df['SMA'] = df['close'].rolling(window=window).mean()
    df['std_dev'] = df['close'].rolling(window=window).std()
    df['upper_band'] = df['SMA'] + (df['std_dev'] * num_std_dev)
    df['lower_band'] = df['SMA'] - (df['std_dev'] * num_std_dev)
    return df
def macd(df: pd.DataFrame, short_window: int = 12, long_window: int = 26, signal_window: int = 9) -> pd.DataFrame:
    df['EMA_short'] = df['close'].ewm(span=short_window, adjust=False).mean()
    df['EMA_long'] = df['close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    df['Signal_line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    return df
def pct_change(df: pd.DataFrame, periods: int = 1) -> pd.DataFrame:
    df['pct_change'] = df['close'].pct_change(periods=periods) * 100
    return df
def momentum(df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    df['momentum'] = df['close'].diff(periods=window)
    return df
def volatility(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    df['volatility'] = df['close'].rolling(window=window).std()
    return df
def atr(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    df['high_low'] = df['high'] - df['low']
    df['high_close'] = (df['high'] - df['close'].shift()).abs()
    df['low_close'] = (df['low'] - df['close'].shift()).abs()
    df['true_range'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
    df['ATR'] = df['true_range'].rolling(window=window).mean()
    return df
def vwap(df: pd.DataFrame) -> pd.DataFrame:
    df['cum_volume'] = df['volume'].cumsum()
    df['cum_price_volume'] = (df['close'] * df['volume']).cumsum()
    df['VWAP'] = df['cum_price_volume'] / df['cum_volume']
    return df
def obv(df: pd.DataFrame) -> pd.DataFrame:
    df['direction'] = df['close'].diff().apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0)
    df['OBV'] = (df['volume'] * df['direction']).cumsum()
    return df
def adx(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    df['high_diff'] = df['high'].diff()
    df['low_diff'] = df['low'].diff()
    df['tr'] = df[['high_diff', 'low_diff', 'close']].max(axis=1).abs()
    df['+DI'] = 100 * (df['high_diff'].clip(lower=0).rolling(window=window).mean() / df['tr'].rolling(window=window).mean())
    df['-DI'] = 100 * (-df['low_diff'].clip(upper=0).rolling(window=window).mean() / df['tr'].rolling(window=window).mean())
    df['DX'] = 100 * (abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI']))
    df['ADX'] = df['DX'].rolling(window=window).mean()
    return df
def compute_features(df: pd.DataFrame) -> pd.DataFrame:
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
def preprocess_and_detect_trend(data_with_features: pd.DataFrame) -> pd.DataFrame:
    data_with_features['prev_SMA'] = data_with_features['SMA'].shift(1)
    data_with_features['trend'] = data_with_features.apply(detect_trend, axis=1)
    return data_with_features