import sys
import os
import pandas as pd
import glob

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from prediction_ai import train_model

# Step 1: Load and concatenate all CSVs
files = glob.glob("data/raw/*.csv")
dfs = []
for f in files:
    df = pd.read_csv(f)
    # Clean $ from price columns and convert to float
    for col in ['Close/Last', 'Open', 'High', 'Low']:
        df[col] = df[col].replace({r'\$': ''}, regex=True).astype(float)
    # Standardize column names
    df = df.rename(columns={
        'Close/Last': 'close',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Volume': 'volume'
    })
    dfs.append(df)
data = pd.concat(dfs, ignore_index=True)

# Step 2-4: Train the model
model = train_model(data)
print("Model trained and saved as trained_model.pkl")