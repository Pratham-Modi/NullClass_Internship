import pickle
import re
from sklearn.feature_extraction import text
from nltk.stem import WordNetLemmatizer
import nltk

# Ensure necessary NLTK resources are available
try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

try:
    nltk.data.find("corpora/omw-1.4")
except LookupError:
    nltk.download("omw-1.4")

# Load the saved model, vectorizer, and label encoder
with open('sentiment_model.pkl', 'rb') as f:
    model, vectorizer, le = pickle.load(f)

# Initialize stopwords and lemmatizer
stop_words = text.ENGLISH_STOP_WORDS
lemmatizer = WordNetLemmatizer()

# Text cleaning function
def clean_text(text_input):
    text_input = re.sub(r"http\S+", "", text_input)
    text_input = re.sub(r"[^a-zA-Z\s]", "", text_input)
    text_input = text_input.lower()

    words = text_input.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)

# Safe keyword matching
def keyword_match(word, text_input):
    return re.search(rf"\b{re.escape(word)}\b", text_input.lower()) is not None

# Predict sentiment label and confidence
def predict_sentiment(text_input):
    cleaned = clean_text(text_input)
    vector = vectorizer.transform([cleaned])
    probabilities = model.predict_proba(vector)[0]
    prediction = model.predict(vector)[0]
    sentiment = le.inverse_transform([prediction])[0]
    confidence = round(max(probabilities) * 100, 2)

    # Keyword override logic
    override = {
        'positive': ['amazing', 'love', 'excellent', 'happy', 'fantastic', 'superb', 'pleasantly surprised'],
        'negative': ['awful', 'terrible', 'disappointed', 'worst', 'frustrating', 'broken', 'hate'],
        'neutral': ['meeting', 'scheduled', 'plan', 'regular day', 'tomorrow', '10 am']
    }

    for word in override['positive']:
        if keyword_match(word, text_input):
            return 'positive', confidence

    for word in override['negative']:
        if keyword_match(word, text_input):
            return 'negative', confidence

    for word in override['neutral']:
        if keyword_match(word, text_input):
            return 'neutral', confidence

    # Apply confidence threshold
    if confidence < 60:
        return 'neutral', confidence

    return sentiment, confidence
