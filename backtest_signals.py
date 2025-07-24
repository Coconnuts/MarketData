
import pandas as pd
import joblib
from analyse import compute_features, detect_trend
from sklearn.metrics import accuracy_score, classification_report

# Load data
df = pd.read_csv("data/raw/HistoricalData_1753298914633.csv")

# Compute features
features_df = compute_features(df).dropna()

# Label the data with actual trends
features_df['actual_trend'] = features_df.apply(detect_trend, axis=1)

# Prepare features and labels
X = features_df.drop(columns=['close', 'actual_trend'], errors='ignore')
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
