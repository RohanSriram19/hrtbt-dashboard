import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_chat_message(user: str, text: str, emotion: str):
    """
    Insert a chat message into the 'chat_messages' Supabase table.
    """
    data = {
        "user": user,
        "text": text,
        "emotion": emotion
    }
    try:
        supabase.table("chat_messages").insert(data).execute()
    except Exception as e:
        print(f" Error inserting into Supabase: {e}")
