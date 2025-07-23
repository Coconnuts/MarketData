import sys
import os
import pandas as pd
import glob
from prediction_ai import train_model
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from prediction_ai import train_model
# Step 1: Load and concatenate all CSVs
files = glob.glob("data/raw/*.csv")
dfs = [pd.read_csv(f) for f in files]
data = pd.concat(dfs, ignore_index=True)

# Step 2-4: Train the model
model = train_model(data)
print("Model trained and saved as trained_model.pkl")