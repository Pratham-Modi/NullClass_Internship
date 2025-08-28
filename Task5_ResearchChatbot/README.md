# 🔍 Task 5: Research Paper Semantic Search Engine

This project implements a **semantic search engine** for academic papers using a combination of **sentence-level embeddings** and **TF-IDF vectorization** for improved relevance scoring. Users can input natural language queries and receive the top 5 most relevant papers from an arXiv dataset. The frontend is built with **Streamlit**, providing an intuitive and interactive interface to explore research content.

---

## 🚀 Tech Stack

- 🧠 **Sentence Transformers** – Embedding model (`all-MiniLM-L6-v2`)  
- 📈 **TF-IDF Vectorizer** – Classic keyword-based text representation  
- 🐍 **Python** – Core language for backend logic  
- 📊 **Pandas** – Data handling and CSV operations  
- 🔍 **Cosine Similarity** – Ranking results by combined semantic and keyword similarity  
- 🎯 **Streamlit** – UI framework for interactive frontend  
- 📝 **arXiv Dataset** – Subset of academic paper abstracts  

---

## ✨ Features

✅ Natural language query-based paper search  
✅ Combines semantic embeddings and TF-IDF scores for higher accuracy  
✅ Displays **top 5 most relevant papers** with relevance scores  
✅ Outputs include **title**, **authors**, **abstract**, and **relevance score**  
✅ Efficient precomputed embeddings stored as a normalized `.npy` file  
✅ Adjustable alpha parameter to balance TF-IDF vs embedding influence  
✅ Clean, professional, and responsive UI via Streamlit  
✅ Backend caching with `st.cache_data` for improved performance  

---

## 🧱 Final Project Structure

```bash
Task5/
│
├── app.py                 # Streamlit app (frontend logic)
├── requirements.txt       # Required Python packages
├── README.md              # Updated project documentation
├── .gitignore             # Files to ignore in GitHub
│
├── data/
│   ├── arxiv_subset.csv   # Dataset (CSV format)
│   └── data_loader.py     # Script to load/convert/process datasett
│
├── models/
│   └── paper_embeddings.npy  # Precomputed normalized embeddings
│
└── src/
    ├── search_engine.py   # Semantic + TF-IDF hybrid search engine
    └── embedder.py        # Embedding generation script
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Pratham-Modi/NullClass_Internship/tree/main/Task5_ResearchChatbot
cd NullClassInternship_Task5_PaperSearch
```

### 2. (Optional) Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate     # On Windows
#OR
source venv/bin/activate  # On Linux/macOS
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare Data and Embeddings

Ensure the following files are present/loaded in your project:

- `data/arxiv_subset.csv` → the dataset (CSV format)
- `models/paper_embeddings.npy` → precomputed embeddings

> ⚠️ After loading these files in the app, if any prompt pops up, **click "Ignore"** and **do not click "Update Changes"**.

### 5. Run the App

```bash
streamlit run app.py
```

---

## ⚙️ How It Works

- The embedder.py script generates semantic embeddings from paper titles and abstracts using SentenceTransformer and saves them as a normalized .npy file.
- The search_engine.py loads the dataset, embeddings, and initializes a TF-IDF vectorizer on the paper texts.
- When a user inputs a query, the engine encodes it with the same SentenceTransformer model and vectorizes it with TF-IDF.
- The engine computes cosine similarity scores between the query and paper embeddings, as well as TF-IDF vectors.
- These scores are combined using a weighted sum controlled by the alpha parameter (default 0.5), balancing semantic and keyword-based similarity.
- The top results are returned and displayed in the Streamlit app with paper metadata and relevance scores.

---

## 📦 requirements.txt

```bash
streamlit
numpy
pandas
scikit-learn
sentence-transformers
```

---

## 📌 Additional Notes

- Before running the Streamlit app, make sure the CSV dataset and the precomputed embeddings are available.
- If the app shows a message after loading these files, **click "Ignore"**; do not click "Update Changes".
- Embeddings and TF-IDF matrices are normalized for consistent cosine similarity calculations.
- The alpha parameter can be tuned (range 0 to 1) to give more weight to either TF-IDF (closer to 1) or semantic similarity (closer to 0), improving relevance based on use case.
- The UI includes helpful tips and a sidebar for better user experience.
- The project uses st.cache_data to cache model loading and embeddings for faster repeated queries.

---

## 👨‍💻 Developed By

Pratham Modi  
📅 August 2025
