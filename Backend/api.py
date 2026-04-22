# import os
# from flask import Flask, jsonify, request
# from pymongo import MongoClient
# from dotenv import load_dotenv
# from datetime import datetime, timedelta, timezone

# # 1. Load Secure Environment Variables
# load_dotenv()

# app = Flask(__name__)

# # 2. Connect to MongoDB Atlas
# MONGO_URI = os.getenv("MONGO_URI")
# mongo_client = MongoClient(MONGO_URI)
# db = mongo_client["climapredict_db"]
# collection = db["sensor_logs"]

# # --- ENDPOINT 0: ROOT/WELCOME ---
# @app.route('/', methods=['GET'])
# def index():
#     return jsonify({
#         "status": "success", 
#         "message": "Welcome to ClimaPredict API!",
#         "endpoints": ["/api/latest", "/api/history"]
#     }), 200

# # --- ENDPOINT 1: LIVE GAUGES ---
# @app.route('/api/latest', methods=['GET'])
# def get_latest_data():
#     """Fetches the absolute newest sensor reading."""
#     try:
#         # Sort by timestamp descending (-1) and grab the first one
#         latest = collection.find_one({}, sort=[("server_timestamp", -1)])
        
#         if latest:
#             latest['_id'] = str(latest['_id']) # Remove un-serializable Mongo ID
#             return jsonify({"status": "success", "data": latest}), 200
#         else:
#             return jsonify({"status": "error", "message": "No data found in database"}), 404
            
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


# # --- ENDPOINT 2: CHARTS & ML PREDICTIONS ---
# @app.route('/api/history', methods=['GET'])
# def get_history():
#     """Fetches historical data for the last X hours (defaults to 24)."""
#     try:
#         # Check if the frontend asked for a specific number of hours
#         hours = int(request.args.get('hours', 24))
        
#         # Calculate the time threshold
#         time_threshold = datetime.now(timezone.utc) - timedelta(hours=hours)
        
#         # Query Mongo for everything newer than the threshold
#         cursor = collection.find(
#             {"server_timestamp": {"$gte": time_threshold.isoformat()}},
#             {"_id": 0} 
#         ).sort("server_timestamp", 1) # Sort chronologically (oldest to newest) for plotting
        
#         data = list(cursor)
#         return jsonify({"status": "success", "count": len(data), "data": data}), 200
        
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


# if __name__ == '__main__':
#     print("🚀 Starting ClimaPredict REST API on http://127.0.0.1:5000 ...")
#     app.run(debug=True, port=5000)







import os
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import joblib

# 1. Load Secure Environment Variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# 2. Connect to MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["climapredict_db"]
collection = db["sensor_logs"]

# 3. Load the Trained Machine Learning Models
print("Loading Machine Learning Models...")
try:
    anomaly_model = joblib.load('anomaly_model.pkl')
    forecast_model = joblib.load('forecast_model.pkl')
    print("✅ ML Models loaded successfully!")
except Exception as e:
    print(f"⚠️ Warning: ML models not found. Run advanced_ml.py first. Error: {e}")
    anomaly_model = None
    forecast_model = None

# --- ENDPOINT 0: ROOT/WELCOME ---
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "success", 
        "message": "Welcome to ClimaPredict API!",
        "endpoints": ["/api/latest", "/api/history"]
    }), 200

# --- ENDPOINT 1: LIVE GAUGES & ML PREDICTIONS ---
@app.route('/api/latest', methods=['GET'])
def get_latest_data():
    """Fetches the absolute newest sensor reading and runs it through the AI."""
    try:
        latest = collection.find_one({}, sort=[("server_timestamp", -1)])
        
        if latest:
            latest['_id'] = str(latest['_id']) # Remove un-serializable Mongo ID
            
            # --- APPLY MACHINE LEARNING ---
            # Default ML block in case sensors are still warming up
            latest["ml_insights"] = {
                "is_anomaly": False,
                "predicted_co2_1hr": None
            }
            
            # Extract current sensor values
            temp = latest.get("dht22", {}).get("temperature")
            hum = latest.get("dht22", {}).get("humidity")
            pressure = latest.get("bmp280", {}).get("pressure_hpa")
            co2 = latest.get("ens160", {}).get("eco2")
            
            # Only run AI predictions if the ENS160 gas sensor has finished its 3-min warmup
            if co2 and anomaly_model and forecast_model:
                # Task 1: Anomaly Detection
                features_anomaly = pd.DataFrame([[temp, hum, co2]], columns=['temperature', 'humidity', 'eco2'])
                is_anomaly = anomaly_model.predict(features_anomaly)[0] == -1
                
                # Task 2: 1-Hour Future Prediction
                features_forecast = pd.DataFrame([[temp, hum, pressure, co2]], columns=['temperature', 'humidity', 'pressure', 'eco2'])
                predicted_co2 = forecast_model.predict(features_forecast)[0]
                
                # Attach AI findings to the JSON payload
                latest["ml_insights"]["is_anomaly"] = bool(is_anomaly)
                latest["ml_insights"]["predicted_co2_1hr"] = round(float(predicted_co2), 1)

            return jsonify({"status": "success", "data": latest}), 200
        else:
            return jsonify({"status": "error", "message": "No data found in database"}), 404
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# --- ENDPOINT 2: CHARTS (HISTORY) ---
@app.route('/api/history', methods=['GET'])
def get_history():
    """Fetches historical data for the last X hours (defaults to 24)."""
    try:
        hours = int(request.args.get('hours', 24))
        time_threshold = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        cursor = collection.find(
            {"server_timestamp": {"$gte": time_threshold.isoformat()}},
            {"_id": 0} 
        ).sort("server_timestamp", 1) 
        
        data = list(cursor)
        return jsonify({"status": "success", "count": len(data), "data": data}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    print("🚀 Starting ClimaPredict REST API with ML on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)