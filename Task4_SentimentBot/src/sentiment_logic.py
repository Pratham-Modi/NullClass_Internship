# src/sentiment_logic.py

import pickle
import os
import re
import string

# Path to the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'sentiment_model.pkl')

# Load the model, vectorizer, and label encoder
with open(MODEL_PATH, 'rb') as f:
    model_data = pickle.load(f)
    model = model_data['model']
    vectorizer = model_data['vectorizer']
    label_encoder = model_data['label_encoder']

def preprocess_text(text):
    """
    Preprocess the input text:
    - Convert to lowercase
    - Remove punctuation
    - Remove extra whitespace
    """
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def predict_sentiment(text):
    """
    Predict the sentiment of the given text.
    Returns the label as a string (e.g., 'Positive', 'Negative', 'Neutral')
    """
    text = preprocess_text(text)
    text_vector = vectorizer.transform([text])
    pred = model.predict(text_vector)
    label = label_encoder.inverse_transform(pred)[0]
    return label
