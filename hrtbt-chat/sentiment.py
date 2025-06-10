import text2emotion as t2e

def classify_emotion(text):
    """
    Returns the dominant emotion from the text.
    One of: Happy, Angry, Surprise, Sad, Fear
    If no emotion is found, returns 'neutral'
    """
    emotions = t2e.get_emotion(text)

    if not emotions or sum(emotions.values()) == 0:
        return 'neutral'

    # Get the emotion with the highest score
    dominant_emotion = max(emotions, key=emotions.get)
    return dominant_emotion.lower()
