import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

print("1. Simulating 1 Year of Kaggle-style Sensor Data...")
# Simulating 35,000 rows (approx 1 year of 15-min intervals)
np.random.seed(42)
n_samples = 35000
data = {
    'temperature': np.random.normal(24, 2, n_samples),
    'humidity': np.random.normal(55, 10, n_samples),
    'co2': np.random.normal(600, 150, n_samples),
    'dust': np.random.normal(15, 5, n_samples)
}
df = pd.DataFrame(data)

df.loc[df.sample(frac=0.05).index, 'co2'] = np.nan
df = df.fillna(method='ffill') 

print("2. Feature Engineering: Calculating Future CO2 Targets...")
# predict the CO2 level 1 hour (4 intervals of 15 mins) in the future
df['target_co2_1hr_future'] = df['co2'].shift(-4)
df = df.dropna() # Drop the last 4 rows that have no future target

# Features (X) and Target (y)
X = df[['temperature', 'humidity', 'co2', 'dust']]
y = df['target_co2_1hr_future']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("3. Training the Random Forest Predictive Model...")
# chose Random Forest because it handles non-linear IoT sensor relationships better than basic linear regression."
model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
print(f"Model Training Complete! Root Mean Squared Error: {rmse:.2f} ppm")

print("4. Saving Model to Disk...")
joblib.dump(model, 'climapredict_rf_model.pkl')
print("Saved as 'climapredict_rf_model.pkl'. Ready for live backend!")