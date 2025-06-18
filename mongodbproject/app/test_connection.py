from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/")
    db_list = client.list_database_names()
    print("✅ Connected to MongoDB successfully!")
    print("📚 Existing databases:", db_list)
except Exception as e:
    print("❌ Failed to connect to MongoDB:", e)
