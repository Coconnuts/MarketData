from analyse import compute_features
from analyse import detect_trend
import joblib
from sklearn.ensemble import RandomForestClassifier

def label_data(data):
    data_with_features = compute_features(data)
    data_with_features['prev_SMA'] = data_with_features['SMA'].shift(1)
    data_with_features['trend'] = data_with_features.apply(detect_trend, axis=1)
    return data_with_features
def train_model(data):
    data = label_data(data).dropna()

    features = data.drop(columns=[col for col in ['close', 'trend', 'Date'] if col in data.columns])
    features = features.select_dtypes(include='number')
    labels = data['trend']

    model = RandomForestClassifier(n_estimators=100, random_state=50)
    model.fit(features, labels)

    joblib.dump(model, 'trained_model.pkl')
    return model