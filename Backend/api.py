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






#  ----------------Chatbot 1st(working but not responding to user qustion)-------
# import os
# import pandas as pd
# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from pymongo import MongoClient
# from dotenv import load_dotenv
# from datetime import datetime, timedelta, timezone
# import joblib
# import google.generativeai as genai
# import json

# # 1. Load Secure Environment Variables
# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# # 2. Connect to MongoDB Atlas
# MONGO_URI = os.getenv("MONGO_URI")
# mongo_client = MongoClient(MONGO_URI)
# db = mongo_client["climapredict_db"]
# collection = db["sensor_logs"]

# # Configure Gemini for AI Chat
# GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
# if GENAI_API_KEY:
#     genai.configure(api_key=GENAI_API_KEY)
# else:
#     print("⚠️ Warning: GEMINI_API_KEY not found in .env. Chatbot will not work.")

# # 3. Load the Trained Machine Learning Models
# print("Loading Machine Learning Models...")
# try:
#     anomaly_model = joblib.load('anomaly_model.pkl')
#     forecast_model = joblib.load('forecast_model.pkl')
#     print("✅ ML Models loaded successfully!")
# except Exception as e:
#     print(f"⚠️ Warning: ML models not found. Run advanced_ml.py first. Error: {e}")
#     anomaly_model = None
#     forecast_model = None

# # --- ENDPOINT 0: ROOT/WELCOME ---
# @app.route('/', methods=['GET'])
# def index():
#     return jsonify({
#         "status": "success", 
#         "message": "Welcome to ClimaPredict API!",
#         "endpoints": ["/api/latest", "/api/history"]
#     }), 200

# # --- ENDPOINT 1: LIVE GAUGES & ML PREDICTIONS ---
# @app.route('/api/latest', methods=['GET'])
# def get_latest_data():
#     """Fetches the absolute newest sensor reading and runs it through the AI."""
#     try:
#         latest = collection.find_one({}, sort=[("server_timestamp", -1)])
        
#         if latest:
#             latest['_id'] = str(latest['_id']) # Remove un-serializable Mongo ID
            
#             # --- APPLY MACHINE LEARNING ---
#             # Default ML block in case sensors are still warming up
#             latest["ml_insights"] = {
#                 "is_anomaly": False,
#                 "predicted_co2_1hr": None
#             }
            
#             # Extract current sensor values
#             temp = latest.get("dht22", {}).get("temperature")
#             hum = latest.get("dht22", {}).get("humidity")
#             pressure = latest.get("bmp280", {}).get("pressure_hpa")
#             co2 = latest.get("ens160", {}).get("eco2")
            
#             # Only run AI predictions if the ENS160 gas sensor has finished its 3-min warmup
#             if co2 and anomaly_model and forecast_model:
#                 # Task 1: Anomaly Detection
#                 features_anomaly = pd.DataFrame([[temp, hum, co2]], columns=['temperature', 'humidity', 'eco2'])
#                 is_anomaly = anomaly_model.predict(features_anomaly)[0] == -1
                
#                 # Task 2: 1-Hour Future Prediction
#                 features_forecast = pd.DataFrame([[temp, hum, pressure, co2]], columns=['temperature', 'humidity', 'pressure', 'eco2'])
#                 predicted_co2 = forecast_model.predict(features_forecast)[0]
                
#                 # Attach AI findings to the JSON payload
#                 latest["ml_insights"]["is_anomaly"] = bool(is_anomaly)
#                 latest["ml_insights"]["predicted_co2_1hr"] = round(float(predicted_co2), 1)

#             return jsonify({"status": "success", "data": latest}), 200
#         else:
#             return jsonify({"status": "error", "message": "No data found in database"}), 404
            
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


# # --- ENDPOINT 2: CHARTS (HISTORY) ---
# @app.route('/api/history', methods=['GET'])
# def get_history():
#     """Fetches historical data for the last X hours (defaults to 24)."""
#     try:
#         hours = int(request.args.get('hours', 24))
#         time_threshold = datetime.now(timezone.utc) - timedelta(hours=hours)
        
#         cursor = collection.find(
#             {"server_timestamp": {"$gte": time_threshold.isoformat()}},
#             {"_id": 0} 
#         ).sort("server_timestamp", 1) 
        
#         data = list(cursor)
#         return jsonify({"status": "success", "count": len(data), "data": data}), 200
        
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


# # --- ENDPOINT 3: AI CHAT WIDGET ---
# def get_dataset_summary():
#     # Placeholder for the future dataset connection
#     return "Dataset summary: Contains historical records from sensors. Trends show higher CO2 during daytime."

# @app.route('/api/chat', methods=['POST'])
# def chat_with_ai():
#     try:
#         if not GENAI_API_KEY:
#             return jsonify({"status": "error", "message": "Gemini API key is not configured on the server."}), 500

#         data = request.json
#         user_msg = data.get('message', '')
#         history = data.get('history', [])
#         dashboard_state = data.get('dashboard_state', {})

#         dataset_summary = get_dataset_summary()

#         # Build context from dashboard state
#         state_context = f"Current Dashboard Tab: {dashboard_state.get('tab')}\\nLatest Sensor Readings: {dashboard_state.get('lastReading', {})}\\nActive Alerts/AI Insights: {dashboard_state.get('mlInsights', {})}\\nDataset Context: {dataset_summary}"

#         system_prompt = f"You are the ClimaPredict AI Assistant, integrated directly into a dashboard.\\nYour goal is to help users analyze environmental sensor data.\\nUse the current state of the dashboard below to ground your answers:\\n{state_context}\\n\\nBe concise, technical but accessible, and directly refer to the active data if relevant."

#         # Build Gemini Chat History format
#         gemini_history = []
#         for msg in history[:-1]:  # Exclude the very last user message because we pass it separately
#             role = 'user' if msg.get('role') == 'user' else 'model'
#             # Skip errors from history mapping
#             if msg.get('role') == 'error':
#                 continue
#             gemini_history.append({"role": role, "parts": [msg.get('text', '')]})

#         model = genai.GenerativeModel(
#             model_name="gemini-1.5-flash", 
#             system_instruction=system_prompt
#         )
        
#         chat = model.start_chat(history=gemini_history)
#         response = chat.send_message(user_msg)

#         return jsonify({"status": "success", "reply": response.text}), 200

#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return jsonify({"status": "error", "message": f"AI service error: {str(e)}"}), 500

# if __name__ == '__main__':
#     print("🚀 Starting ClimaPredict REST API with ML on http://127.0.0.1:5000 ...")
#     app.run(debug=True, port=5000)


import os
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import joblib
from google import genai
from google.genai import types

# 1. Load Secure Environment Variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# 2. Connect to MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["climapredict_db"]
collection = db["sensor_logs"]

# Configure Gemini using the NEW SDK
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
if GENAI_API_KEY:
    ai_client = genai.Client(api_key=GENAI_API_KEY)
else:
    ai_client = None
    print("⚠️ Warning: GEMINI_API_KEY not found in .env. Chatbot will not work.")

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
            
            # Default ML block in case sensors are still warming up
            latest["ml_insights"] = {
                "is_anomaly": False,
                "predicted_co2_1hr": None
            }
            
            # Extract current sensor values safely
            temp = latest.get("dht22", {}).get("temperature", 0)
            hum = latest.get("dht22", {}).get("humidity", 0)
            pressure = latest.get("bmp280", {}).get("pressure_hpa", 1000)
            co2 = latest.get("ens160", {}).get("eco2")
            
            if co2 and anomaly_model and forecast_model:
                try:
                    features_anomaly = pd.DataFrame([[temp, hum, co2]], columns=['temperature', 'humidity', 'eco2'])
                    is_anomaly = anomaly_model.predict(features_anomaly)[0] == -1
                    
                    features_forecast = pd.DataFrame([[temp, hum, pressure, co2]], columns=['temperature', 'humidity', 'pressure', 'eco2'])
                    predicted_co2 = forecast_model.predict(features_forecast)[0]
                    
                    latest["ml_insights"]["is_anomaly"] = bool(is_anomaly)
                    latest["ml_insights"]["predicted_co2_1hr"] = round(float(predicted_co2), 1)
                except Exception as ml_err:
                    print(f"⚠️ AI Prediction Error: {ml_err}")

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


# --- ENDPOINT 3: AI CHAT WIDGET & MONGODB HOOK ---
# def get_dataset_summary():
#     """Dynamically queries MongoDB to give the chatbot historical context."""
#     try:
#         # Fetch the last 100 sensor readings
#         cursor = collection.find({}, {"_id": 0}).sort("server_timestamp", -1).limit(100)
#         data = list(cursor)
        
#         if not data:
#             return "No historical data available yet."
            
#         # Calculate statistical averages for the prompt
#         temps = [d.get("dht22", {}).get("temperature") for d in data if d.get("dht22", {}).get("temperature") is not None]
#         co2s = [d.get("ens160", {}).get("eco2") for d in data if d.get("ens160", {}).get("eco2") is not None]
        
#         avg_temp = round(sum(temps) / len(temps), 1) if temps else "N/A"
#         avg_co2 = round(sum(co2s) / len(co2s), 1) if co2s else "N/A"
#         max_co2 = max(co2s) if co2s else "N/A"
        
#         return f"Historical Context (Last {len(data)} readings): The average temperature recently has been {avg_temp}°C. The average CO2 is {avg_co2} ppm, hitting a maximum peak of {max_co2} ppm."
    
#     except Exception as e:
#         return f"Database error: {str(e)}"

# --- ENDPOINT 3: AI CHAT WIDGET & MONGODB HOOK ---
def get_dataset_summary():
    """Dynamically queries MongoDB to give the chatbot historical context."""
    try:
        # Fetch the last 100 sensor readings
        cursor = collection.find({}, {"_id": 0}).sort("server_timestamp", -1).limit(100)
        data = list(cursor)
        
        if not data:
            return "No historical data available yet."
            
        # Extract all data points safely
        temps = [d.get("dht22", {}).get("temperature") for d in data if d.get("dht22", {}).get("temperature") is not None]
        hums = [d.get("dht22", {}).get("humidity") for d in data if d.get("dht22", {}).get("humidity") is not None]
        co2s = [d.get("ens160", {}).get("eco2") for d in data if d.get("ens160", {}).get("eco2") is not None]
        pressures = [d.get("bmp280", {}).get("pressure_hpa") for d in data if d.get("bmp280", {}).get("pressure_hpa") is not None]
        
        # Calculate statistical averages for the prompt
        avg_temp = round(sum(temps) / len(temps), 1) if temps else "N/A"
        avg_hum = round(sum(hums) / len(hums), 1) if hums else "N/A"
        avg_co2 = round(sum(co2s) / len(co2s), 1) if co2s else "N/A"
        avg_pressure = round(sum(pressures) / len(pressures), 1) if pressures else "N/A"
        max_co2 = max(co2s) if co2s else "N/A"
        
        # Build the master context string
        return (f"Historical Context (Last {len(data)} readings): "
                f"The average temperature is {avg_temp}°C. "
                f"The average humidity is {avg_hum}%. "
                f"The average atmospheric pressure is {avg_pressure} hPa. "
                f"The average CO2 is {avg_co2} ppm, hitting a maximum peak of {max_co2} ppm.")
    
    except Exception as e:
        return f"Database error: {str(e)}"

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    try:
        if not ai_client:
            return jsonify({"status": "error", "message": "Gemini API key is not configured on the server."}), 500

        data = request.json
        user_msg = data.get('message', '')
        history = data.get('history', [])
        dashboard_state = data.get('dashboard_state', {})

        # Hook into the live MongoDB aggregation
        dataset_summary = get_dataset_summary()

        state_context = f"Current Dashboard Tab: {dashboard_state.get('tab')}\nLatest Sensor Readings: {dashboard_state.get('lastReading', {})}\nActive Alerts/AI Insights: {dashboard_state.get('mlInsights', {})}\nDataset Context: {dataset_summary}"

        system_instruction = f"You are the ClimaPredict AI Assistant, integrated directly into an IoT dashboard.\nAvailable UI tabs are: 'Overview', 'Temperature', 'Humidity', 'Air Quality', and 'Predictive Lab' (this is where AI forecasts and future predictions are).\nYour goal is to help users analyze environmental sensor data.\nUse the current state of the dashboard below to ground your answers:\n{state_context}\n\nBe concise, technical but accessible, and directly refer to the active data if relevant. Explain the data naturally in plain English and do not use exact JSON variable names or technical code flags in your responses. Never hallucinate tabs or features that don't exist."

        # Convert React history into the new Google GenAI SDK format
        formatted_history = []
        for msg in history[:-1]:  
            role = 'user' if msg.get('role') == 'user' else 'model'
            if msg.get('role') == 'error':
                continue
            formatted_history.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg.get('text', ''))])
            )

        # Apply System Prompt configuration
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
        )

        # Execute chat with an experimental fast model to bypass daily quota caps
        chat = ai_client.chats.create(
            # model="gemini-2.5-flash-lite",
            model="gemini-3-flash-preview",
            config=config,
            history=formatted_history
        )
        
        response = chat.send_message(user_msg)

        return jsonify({"status": "success", "reply": response.text}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": f"AI service error: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting ClimaPredict REST API with ML on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)