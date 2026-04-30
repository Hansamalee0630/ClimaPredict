import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
db = client['climapredict_db']
collection = db['sensor_logs_indoor']

print("Finding the high values again...")
docs = list(collection.find({'ens160.eco2': {'$gt': 10000}}))
print("Found count:", len(docs))
if docs:
    print("Deleting them...")
    res = collection.delete_many({'ens160.eco2': {'$gt': 10000}})
    print("Deleted:", res.deleted_count)
