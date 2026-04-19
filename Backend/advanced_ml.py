import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# --- 1. LOAD THE DATASET ---
csv_file = "climapredict_training_data.csv"

print("==================================================")
print("🌿 CLIMAPREDICT: ADVANCED MACHINE LEARNING LAB 🌿")
print("==================================================\n")

if not os.path.exists(csv_file):
    print(f"[WARNING] {csv_file} not found. Did you run export_to_csv.py yet?")
    print("Generating simulated data for testing purposes...\n")
    # Failsafe: Generate dummy data if CSV is missing so the script doesn't crash
    np.random.seed(42)
    n = 2000
    df = pd.DataFrame({
        'temperature': np.random.normal(25, 2, n),
        'humidity': np.random.normal(60, 5, n),
        'pressure': np.random.normal(1012, 1, n),
        'eco2': np.random.normal(500, 100, n)
    })
    # Inject some deliberate anomalies for the AI to find
    df.loc[1500:1520, 'eco2'] = 1800 
    df.loc[1500:1520, 'temperature'] = 32
else:
    print(f"Loading real IoT data from {csv_file}...")
    df = pd.read_csv(csv_file)
    df = df.dropna(subset=['temperature', 'eco2']) # Clean nulls

print(f"Dataset loaded successfully with {len(df)} rows.\n")

# =====================================================================
# RUBRIC REQUIREMENT 1: ANOMALY DETECTION (ISOLATION FOREST)
# =====================================================================
print("--- TASK 1: UNSUPERVISED ANOMALY DETECTION ---")
# Isolation Forest looks for data points that are mathematically "isolated" from normal trends
features_anomaly = df[['temperature', 'humidity', 'eco2']]

iso_forest = IsolationForest(contamination=0.05, random_state=42) # Assume 5% of data is anomalous (spikes)
df['anomaly_flag'] = iso_forest.fit_predict(features_anomaly)

anomalies = df[df['anomaly_flag'] == -1]
print(f"✅ Isolation Forest trained.")
print(f"🔍 Discovered {len(anomalies)} severe environmental anomalies (unnatural spikes).")
print("These spikes usually correlate to doors closing and human occupancy rising.\n")


# =====================================================================
# RUBRIC REQUIREMENT 2: CORRELATION & FEATURE IMPORTANCE
# =====================================================================
print("--- TASK 2: CORRELATION & FEATURE IMPORTANCE ANALYSIS ---")
# We want to know: Which sensor metric impacts CO2 the most?
X_corr = df[['temperature', 'humidity', 'pressure']]
y_corr = df['eco2']

corr_model = RandomForestRegressor(n_estimators=50, random_state=42)
corr_model.fit(X_corr, y_corr)

importances = corr_model.feature_importances_
print("✅ AI Correlation Analysis Complete.")
print("What drives CO2 buildup in the room?")
for feature, imp in zip(X_corr.columns, importances):
    print(f" - {feature.capitalize()}: {imp * 100:.1f}% impact")
print("\n")


# =====================================================================
# RUBRIC REQUIREMENT 3: TEMPORAL TREND ANALYSIS (PREDICTIVE FORECAST)
# =====================================================================
print("--- TASK 3: TEMPORAL TREND FORECASTING (1-HOUR AHEAD) ---")
# Shift the CO2 data back by 4 intervals (Assuming 15min intervals = 1 hour ahead)
df['target_eco2_1hr'] = df['eco2'].shift(-4)
df_train = df.dropna()

X_forecast = df_train[['temperature', 'humidity', 'pressure', 'eco2']]
y_forecast = df_train['target_eco2_1hr']

X_train, X_test, y_train, y_test = train_test_split(X_forecast, y_forecast, test_size=0.2, random_state=42)

forecast_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
forecast_model.fit(X_train, y_train)

predictions = forecast_model.predict(X_test)
r2 = r2_score(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print(f"✅ Predictive Model Trained successfully.")
print(f"📊 Accuracy (R² Score): {r2 * 100:.1f}%")
print(f"📉 Average Error (RMSE): ±{rmse:.1f} ppm")

# Save the models for the API to use later
joblib.dump(iso_forest, 'anomaly_model.pkl')
joblib.dump(forecast_model, 'forecast_model.pkl')
print("\n💾 Models saved successfully as .pkl files! Ready for API integration.")
print("==================================================")