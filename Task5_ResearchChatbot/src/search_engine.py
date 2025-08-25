import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PaperSearchEngine:
    def __init__(self, embeddings_path, csv_path, model_name='sentence-transformers/all-MiniLM-L6-v2', alpha=0.5):
        # Load paper metadata
        self.df = pd.read_csv(csv_path)
        self.df['text'] = self.df['title'].fillna('') + ". " + self.df['abstract'].fillna('')

        # Load embeddings (should be normalized)
        self.embeddings = np.load(embeddings_path)
        self.embeddings = self.embeddings / np.linalg.norm(self.embeddings, axis=1, keepdims=True)

        # Load SentenceTransformer model
        self.model = SentenceTransformer(model_name)

        # Setup TF-IDF vectorizer on paper text
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['text'])

        # Alpha controls balance between tf-idf and semantic similarity (0 to 1)
        self.alpha = alpha

    def embed_query(self, query):
        query_emb = self.model.encode([query])
        query_emb = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)
        return query_emb

    def search(self, query, top_k=5):
        # Embeddings similarity
        query_embedding = self.embed_query(query)
        sem_scores = cosine_similarity(query_embedding, self.embeddings)[0]

        # TF-IDF similarity
        tfidf_query_vec = self.vectorizer.transform([query])
        tfidf_scores = cosine_similarity(tfidf_query_vec, self.tfidf_matrix).flatten()

        # Combine with weighted sum using alpha
        combined_scores = self.alpha * tfidf_scores + (1 - self.alpha) * sem_scores

        # Get top results indices
        top_indices = combined_scores.argsort()[-top_k:][::-1]

        results = []
        for idx in top_indices:
            results.append({
                'title': self.df.iloc[idx]['title'],
                'abstract': self.df.iloc[idx]['abstract'],
                'score': combined_scores[idx],
                'authors': self.df.iloc[idx].get('authors', 'N/A'),
                # Remove year if mostly missing or comment this line out
                # 'year': self.df.iloc[idx].get('year', 'N/A'),
            })
        return results
