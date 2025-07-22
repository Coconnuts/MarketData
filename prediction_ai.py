from analyse import compute_features
from analyse import detect_trend
import joblib
from sklearn.ensemble import RandomForestClassifier

def label_data(data):
    data_with_features = compute_features(data)
    
    # Labeling based on the trend
    data_with_features['trend'] = data_with_features.apply(lambda row: detect_trend(row), axis=1)
    
    return data_with_features
def train_model(data):
    data = label_data(data).dropna()

    features = data.drop(columns=['close', 'trend'])
    labels = data['trend']

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(features, labels)

    joblib.dump(model, 'trained_model.pkl')
    return model 