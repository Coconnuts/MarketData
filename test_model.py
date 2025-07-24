
import pandas as pd
import joblib
from analyse import compute_features

# Load test historical data
df = pd.read_csv("data/raw/HistoricalData_1753298914633.csv")

# Compute features and clean data
features_df = compute_features(df).dropna()

# Load trained model
model = joblib.load("trained_model.pkl")

# Predict signals
features = features_df.drop(columns=['close'], errors='ignore')  # ensure only features used
predictions = model.predict(features)

# Combine predictions with original data
features_df['predicted_trend'] = predictions

# Output predictions summary
print(features_df[['predicted_trend']].value_counts())
