import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)



client = MongoClient(os.getenv("MONGO_URI"))
db = client["cocktail_app"]

users_collection = db["users"]
posts_collection = db["posts"]
follows_collection = db["follows"]
cocktails_collection = db["cocktails"]

users_collection.create_index("username", unique=True)
users_collection.create_index("email", unique=True)

