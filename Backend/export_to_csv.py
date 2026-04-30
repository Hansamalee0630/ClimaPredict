import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# 1. Load Secure Environment Variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# 2. Connect to MongoDB Atlas
print("Connecting to MongoDB Atlas...")
try:
    client = MongoClient(MONGO_URI)
    db = client["climapredict_db"]
    collection = db["sensor_logs_indoor"]
except Exception as e:
    print(f"[ERROR] Could not connect to database: {e}")
    exit()

print("Fetching data from the cloud. This might take a moment depending on dataset size...")

# 3. Pull all records (excluding the MongoDB internal _id)
cursor = collection.find({}, {"_id": 0})
raw_data = list(cursor)

if len(raw_data) == 0:
    print("\n[WARNING] No data found! Ensure your ESP32 has been running and mqtt_to_mongo.py is active.")
    exit()

print(f"Found {len(raw_data)} total records. Flattening data...")

# 4. Flatten the nested JSON structure for Machine Learning
flat_data = []
for row in raw_data:
    flat_row = {
        "timestamp": row.get("server_timestamp"),
        "temperature": row.get("dht22", {}).get("temperature"),
        "humidity": row.get("dht22", {}).get("humidity"),
        "pressure": row.get("bmp280", {}).get("pressure_hpa"),
        "eco2": row.get("ens160", {}).get("eco2"),
        "tvoc": row.get("ens160", {}).get("tvoc")
    }
    flat_data.append(flat_row)

# 5. Convert to a Pandas DataFrame and save
df = pd.DataFrame(flat_data)

# Sort chronologically just in case
df = df.sort_values(by="timestamp")

filename = "climapredict_training_data.csv"
df.to_csv(filename, index=False)

print(f"\n[SUCCESS] {len(df)} rows exported perfectly to '{filename}'!")
print("This CSV is now ready to be used by train_ml_model.py!")