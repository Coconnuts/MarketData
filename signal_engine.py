from analyse import compute_features
import joblib  # Use plain joblib, not sklearn.externals

model = joblib.load('trained_model.pkl')

def generate_signals(data):
    data_with_features = compute_features(data)

    # Define feature columns FIRST
    feature_columns = [
        'SMA_diff', 'RSI', 'upper_band', 'lower_band', 'MACD', 'Signal_line',
        'pct_change', 'momentum', 'volatility', 'ATR', 'VWAP', 'OBV', '+DI', '-DI', 'ADX'
    ]

    # Drop rows with NaN values in features
    features = data_with_features[feature_columns].dropna()
    if features.empty:
        return None  # Not enough data to compute signals

    # Predict with trained model
    predictions = model.predict(features)
    # Align predictions with original data
    result_df = data_with_features.loc[features.index].copy()
    result_df['predicted_trend'] = predictions

    return result_df[['close', 'predicted_trend']]
def save_signals(signals, filename='signals.csv'):
    if signals is not None and not signals.empty:
        signals.to_csv(filename, index=False)
        print(f"Signals saved to {filename}")
    else:
        print("No signals to save.")
