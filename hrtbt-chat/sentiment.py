from transformers import pipeline
from mongo_client import insert_chat_message

# Load emotion classification pipeline from HuggingFace
emotion_classifier = pipeline("text-classification", model="nateraw/bert-base-uncased-emotion")

def classify_emotion(text):
    """
    Uses BERT to classify the dominant emotion from the input text.
    Returns one of: sadness, joy, love, anger, fear, surprise
    Falls back to 'neutral' if the text is empty or an error occurs.
    """
    if not text.strip():
        return "neutral"

    try:
        result = emotion_classifier(text, truncation=True)[0]
        return result['label'].lower()
    except Exception:
        return "neutral"

def classify_and_store(username, text):
    """
    Classifies emotion and stores the result in MongoDB.
    Returns the classified emotion.
    """
    emotion = classify_emotion(text)
    insert_chat_message(username, text, emotion)
    return emotion
