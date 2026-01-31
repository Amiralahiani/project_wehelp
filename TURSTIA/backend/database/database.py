import os
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv

# Load env from backend/.env if present
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

MONGO_URI = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "biocup")

if not MONGO_URI:
    raise RuntimeError("MONGO_URL is not set")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db["users"]
