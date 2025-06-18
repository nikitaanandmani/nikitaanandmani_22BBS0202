from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["library"]
users_collection = db["users"]

def register_user(email, password):
    if users_collection.find_one({"email": email}):
        return False  # User already exists
    users_collection.insert_one({"email": email, "password": password})
    return True

def login_user(email, password):
    user = users_collection.find_one({"email": email, "password": password})
    return user is not None
