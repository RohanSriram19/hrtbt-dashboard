from mongo_client import insert_chat_message

inserted_id = insert_chat_message("gotyadawg11", "Where's that lip reading girl on TikTok", "anger")
print("Inserted with ID:", inserted_id)

