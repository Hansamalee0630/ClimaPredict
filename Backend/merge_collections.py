import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load Environment Variables
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=env_path)

# MongoDB Config
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "climapredict_db"
TARGET_COLLECTION = "sensor_logs_indoor"
SOURCE_COLLECTIONS = ["sensor_logs", "sensor_logs_test"]

print("Connecting to MongoDB Atlas...")
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[DB_NAME]
    target_collection = db[TARGET_COLLECTION]
    mongo_client.admin.command('ping')
    print("[SUCCESS] Connected to MongoDB Atlas Cloud!")
except Exception as e:
    print(f"[ERROR] Could not connect to MongoDB: {e}")
    exit()

total_inserted = 0

for source in SOURCE_COLLECTIONS:
    source_collection = db[source]
    count = source_collection.count_documents({})
    print(f"\n[*] Found {count} documents in '{source}'.")
    
    if count > 0:
        docs = list(source_collection.find({}))
        
        # Remove '_id' to avoid duplicate key errors during insertion
        for doc in docs:
            if '_id' in doc:
                del doc['_id']
                
        try:
            result = target_collection.insert_many(docs)
            inserted_count = len(result.inserted_ids)
            total_inserted += inserted_count
            print(f"[+] Successfully merged {inserted_count} documents from '{source}' into '{TARGET_COLLECTION}'.")
        except Exception as e:
            print(f"[ERROR] Failed to insert documents from '{source}': {e}")
    else:
         print(f"[-] Skipping '{source}' as it is empty.")

print(f"\n[SUCCESS] Merge operation completed. Total documents inserted into '{TARGET_COLLECTION}': {total_inserted}")
