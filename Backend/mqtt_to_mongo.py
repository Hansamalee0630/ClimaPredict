import os
import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime, timezone
from dotenv import load_dotenv

# 1. Load Secure Environment Variables
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=env_path)

# 2. --- MONGODB CONFIGURATION ---
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "climapredict_db"
COLLECTION_NAME = "sensor_logs"

print("Connecting to MongoDB Atlas...")
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[DB_NAME]
    collection = db[COLLECTION_NAME]
    # Quick ping to verify connection
    mongo_client.admin.command('ping')
    print("[SUCCESS] Connected to MongoDB Atlas Cloud!")
except Exception as e:
    print(f"[ERROR] Could not connect to MongoDB: {e}")
    exit()

# 3. Configure MQTT Settings
MQTT_BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
MQTT_PORT = 1883
MQTT_TOPIC = "sliit/climapredict/hansa_node_1"

# --- CORE FUNCTIONS ---

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[SUCCESS] Connected to HiveMQ Broker!")
        client.subscribe(MQTT_TOPIC)
        print(f"[*] Subscribed and listening to topic: {MQTT_TOPIC}")
    else:
        print(f"[ERROR] Failed to connect to HiveMQ, return code {rc}")

def on_message(client, userdata, msg):
    try:
        # Parse the JSON payload from the ESP32
        payload_str = msg.payload.decode('utf-8')
        sensor_data = json.loads(payload_str)
        
        # Add a proper UTC server timestamp for Time-Series ML training later
        sensor_data["server_timestamp"] = datetime.now(timezone.utc).isoformat()
        
        # Insert into MongoDB NoSQL Database
        inserted_id = collection.insert_one(sensor_data).inserted_id
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Data saved to Atlas! Temp: {sensor_data.get('dht22', {}).get('temperature')}°C | eCO2: {sensor_data.get('ens160', {}).get('eco2')}ppm")
        
    except json.JSONDecodeError:
        print("[WARNING] Received invalid JSON format.")
    except Exception as e:
        print(f"[ERROR] Error processing message: {e}")

# --- START THE BRIDGE ---
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

print(f"Connecting to MQTT Broker: {MQTT_BROKER}...")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Loop forever, listening for ESP32 data and saving to the cloud
try:
    print("Bridge is active. Press Ctrl+C to stop.")
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("\nIngestion Service Stopped by User.")