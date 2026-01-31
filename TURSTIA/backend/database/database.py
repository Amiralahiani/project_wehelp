from pymongo import MongoClient

MONGO_URI = "mongodb+srv://trustia_admin:acYKnOSliVwUq0wm@trustia.a1cns83.mongodb.net/?appName=TRUSTIA"
client = MongoClient(MONGO_URI)
db = client["trustia_auth"]
users_collection = db["users"]
