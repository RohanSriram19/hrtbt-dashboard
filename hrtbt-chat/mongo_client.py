from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables if using .env
load_dotenv()

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://rohansriram19:Seahawk24!@hrtbt-cluster.ohq38kz.mongodb.net/hrtbt?retryWrites=true&w=majority&appName=hrtbt-cluster")

client = MongoClient(MONGO_URI)

db = client["hrtbt"]
chat_collection = db["chat_messages"]

def insert_chat_message(username, message, emotion):
    doc = {
        "username": username,
        "message": message,
        "emotion": emotion
    }
    result = chat_collection.insert_one(doc)
    return result.inserted_id
