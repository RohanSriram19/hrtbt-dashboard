from transformers import pipeline

# Load emotion classification pipeline from HuggingFace
emotion_classifier = pipeline("text-classification", model="nateraw/bert-base-uncased-emotion")

def classify_emotion(text):
    """
    Uses BERT to classify the dominant emotion from the input text.

    Returns one of: sadness, joy, love, anger, fear, surprise
    """
    if not text.strip():
        return "neutral"

    try:
        result = emotion_classifier(text, truncation=True)[0]
        return result['label'].lower()
    except Exception:
        return "neutral"
