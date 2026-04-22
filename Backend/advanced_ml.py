import pandas as pd
import joblib
import json
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

print("Starting ClimaPredict ML Training Pipeline...")

# 1. Load the Dataset
print("Loading dataset: climapredict_training_data.csv...")
try:
    df = pd.read_csv('climapredict_training_data.csv')
except FileNotFoundError:
    print(" Error: CSV not found. Please run export_to_csv.py first.")
    exit()

# Clean data: Remove any rows with missing sensor readings
df = df.dropna(subset=['temperature', 'humidity', 'pressure', 'eco2'])

if len(df) < 50:
    print(" Not enough data to train models. Keep your sensors running longer!")
    exit()

# ---------------------------------------------------------
# REQUIREMENT 1: ANOMALY DETECTION (Isolation Forest)
# ---------------------------------------------------------
print("\n Training Anomaly Detection Model (Isolation Forest)...")
features_anomaly = ['temperature', 'humidity', 'eco2']
X_anomaly = df[features_anomaly]

# Contamination represents the percentage of outliers we expect (e.g., 5%)
iso_forest = IsolationForest(contamination=0.05, random_state=42)
iso_forest.fit(X_anomaly)

joblib.dump(iso_forest, 'anomaly_model.pkl')
print("✅ anomaly_model.pkl saved.")

# ---------------------------------------------------------
# REQUIREMENT 2: TEMPORAL FORECASTING (Random Forest)
# ---------------------------------------------------------
print("\n Training Temporal Forecasting Model (Random Forest)...")
# For our dry run, we simulate the "future" CO2 by shifting the data 
# (e.g., predicting 50 data points ahead)
df['eco2_future'] = df['eco2'].shift(-50) 
df_rf = df.dropna()

features_rf = ['temperature', 'humidity', 'pressure', 'eco2']
X_rf = df_rf[features_rf]
y_rf = df_rf['eco2_future']

X_train, X_test, y_train, y_test = train_test_split(X_rf, y_rf, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

mse = mean_squared_error(y_test, rf_model.predict(X_test))
print(f"Random Forest MSE (Error Rate): {mse:.2f} ppm")

joblib.dump(rf_model, 'forecast_model.pkl')
print("✅ forecast_model.pkl saved.")

# ---------------------------------------------------------
# REQUIREMENT 3: SENSOR CORRELATION (Feature Importance)
# ---------------------------------------------------------
print("\n Extracting Sensor Correlation & Feature Importance...")
# The Random Forest automatically calculates which sensors had the biggest impact
importances = rf_model.feature_importances_

feature_importance_dict = {
    "features": features_rf,
    "importances": [float(i) for i in importances]
}

# Save this to a JSON file so Streamlit can easily read and chart it
with open('feature_importance.json', 'w') as f:
    json.dump(feature_importance_dict, f)

print("✅ feature_importance.json saved.")
print("\n All Machine Learning pipelines executed successfully!")