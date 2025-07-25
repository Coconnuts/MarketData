import glob
import pandas as pd
import joblib
from analyse import compute_features, detect_trend
from sklearn.metrics import accuracy_score, classification_report

# Load data
df = pd.concat([pd.read_csv(f) for f in glob.glob("data/testing/*.csv")], ignore_index=True)

# Clean and rename columns to match training
for col in ['Close/Last', 'Open', 'High', 'Low']:
    df[col] = df[col].replace({r'\$': ''}, regex=True).astype(float)
df = df.rename(columns={
    'Close/Last': 'close',
    'Open': 'open',
    'High': 'high',
    'Low': 'low',
    'Volume': 'volume'
})

# Compute features
features_df = compute_features(df).dropna()

# Add prev_SMA for trend detection
features_df['prev_SMA'] = features_df['SMA'].shift(1)
features_df = features_df.dropna(subset=['prev_SMA'])  # Ensure no NaN in prev_SMA
features_df['actual_trend'] = features_df.apply(detect_trend, axis=1)

# Prepare features and labels
X = features_df.drop(columns=['close', 'actual_trend'], errors='ignore')
X = X.select_dtypes(include='number')
y_true = features_df['actual_trend']

# Load trained model
model = joblib.load("trained_model.pkl")

# Predict
y_pred = model.predict(X)
features_df['predicted_trend'] = y_pred

# Evaluate
print("Accuracy:", accuracy_score(y_true, y_pred))
print("Detailed classification report:")
print(classification_report(y_true, y_pred))
