import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
db = client['climapredict_db']
collection = db['sensor_logs_indoor']

# Find documents with extremely high CO2
print("Searching for high CO2 readings (> 10000 ppm)...")
docs = collection.find({'ens160.eco2': {'$gt': 10000}}).sort('server_timestamp', 1)
count = 0
for doc in docs:
    count += 1
    print(f"Time: {doc.get('server_timestamp')} | eCO2: {doc.get('ens160', {}).get('eco2')} | Temp: {doc.get('dht22', {}).get('temperature')} | Hum: {doc.get('dht22', {}).get('humidity')}")

print(f"Total abnormal readings found: {count}")
