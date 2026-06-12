from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client.phantomguard

# Collections
users_collection = db["users"]         # stores registered owners
devices_collection = db["devices"]     # stores device info + pusher channel
evidence_collection = db["evidence"]   # stores thief photo + wifi data
backup_collection = db["backup"]       # stores contacts, SMS, photos backup

def get_db():
    return db