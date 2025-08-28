import pickle
import re
from sklearn.feature_extraction import text
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')

with open('sentiment_model.pkl', 'rb') as f:
    model, vectorizer, le = pickle.load(f)

stop_words = set(stopwords.words('english')).union(text.ENGLISH_STOP_WORDS)
lemmatizer = WordNetLemmatizer()

# Text preprocessing
def clean_text(text_input):
    """Clean and preprocess user input."""
    text_input = re.sub(r"http\S+", "", text_input)  # remove URLs
    text_input = re.sub(r"[^a-zA-Z\s]", "", text_input)  # remove punctuation/numbers
    text_input = text_input.lower()
    words = text_input.split()
    
    cleaned_words = []
    for word in words:
        if word not in stop_words:
            try:
                cleaned_words.append(lemmatizer.lemmatize(word))
            except:
                cleaned_words.append(word)
    return " ".join(cleaned_words)

# Sentiment analysis
def analyze_sentiment(text_input):
    """Predict sentiment and return label + confidence."""
    if not text_input.strip():
        return {"label": "NEUTRAL", "score": 0.0}

    cleaned = clean_text(text_input)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    probabilities = model.predict_proba(vector)[0]

    sentiment_label = le.inverse_transform([prediction])[0]
    confidence = round(max(probabilities) * 100, 2)

    return {"label": sentiment_label.upper(), "score": confidence}
