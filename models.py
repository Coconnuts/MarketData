import sys
import os
import pandas as pd
import glob
from analyse import compute_features

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from prediction_ai import train_model

# Step 1: Load and concatenate all CSVs
files = glob.glob("data/raw/*.csv")
dfs = []
for f in files:
    df = pd.read_csv(f)
    for col in ['Close/Last', 'Open', 'High', 'Low']:
        df[col] = df[col].replace({r'\$': ''}, regex=True).astype(float)
    df = df.rename(columns={
        'Close/Last': 'close',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Volume': 'volume'
    })
    dfs.append(df)
data = pd.concat(dfs, ignore_index=True)
data = compute_features(data)

# Train the model (RandomForestClassifier)
model = train_model(data)
print("Model trained and saved as trained_model.pkl")