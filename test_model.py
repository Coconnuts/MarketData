import glob
import pandas as pd
import joblib
from analyse import compute_features

# Load test historical data
df = pd.concat([pd.read_csv(f) for f in glob.glob("data/testing/*.csv")], ignore_index=True)

# Clean and rename columns as in models.py
for col in ['Close/Last', 'Open', 'High', 'Low']:
    df[col] = df[col].replace({r'\$': ''}, regex=True).astype(float)
df = df.rename(columns={
    'Close/Last': 'close',
    'Open': 'open',
    'High': 'high',
    'Low': 'low',
    'Volume': 'volume'
})

# Compute features and clean data
features_df = compute_features(df).dropna()

# Add prev_SMA to match training features
features_df['prev_SMA'] = features_df['SMA'].shift(1)

# Drop rows with NaN in prev_SMA (to match training dropna)
features_df = features_df.dropna(subset=['prev_SMA'])

# Load trained model
model = joblib.load("trained_model.pkl")

# Select only numeric columns for prediction (as in train_model)
features = features_df.drop(columns=[col for col in ['close', 'trend', 'Date'] if col in features_df.columns])
features = features.select_dtypes(include='number')

predictions = model.predict(features)

# Combine predictions with original data
features_df['predicted_trend'] = predictions

# If you don't already have actual_trend, create it using your trend labeling logic:
features_df['actual_trend'] = features_df.apply(
    lambda row: 'uptrend' if row['SMA'] > row['prev_SMA'] else
                'downtrend' if row['SMA'] < row['prev_SMA'] else
                'sideways', axis=1
)

# Now compare predictions to actuals
missed = (features_df['predicted_trend'] != features_df['actual_trend']).sum()
total = len(features_df)
print(f"Missed predictions: {missed} out of {total}")
print(f"Accuracy: {(total - missed) / total:.2%}")

# Output predictions summary
print(features_df[['predicted_trend']].value_counts())
