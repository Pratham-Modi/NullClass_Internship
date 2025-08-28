# NullClass Internship – Final Report

## 📌 Internship Information

- **Internship Provider:** NullClass  
- **Intern:** Pratham Modi  
- **Duration:** 25 June 2025 – 25 August 2025 (2 months)  
- **Deliverables:** 5 AI/ML/NLP tasks implemented as per company requirements  

---

## 📂 Repository Structure

```bash
NullClass_Internship/
│
├── Task1_Summarizer/
├── Task2_MultiModalChatbot/
├── Task3_KnowledgeUpdater/
├── Task4_SentimentChatbot/
├── Task5_PaperSearch/
├── README.md                  # This file
└── .gitignore                 # Ignored files (e.g., .vscode/, .env)
```

**Note:** `.vscode/` and `.env` files are excluded from GitHub.

---

## 📝 Tasks Overview

### **Task 1: Extractive Summarizer**

- **Goal:** Implement extractive summarization to generate concise summaries.  
- **Method:** TF-IDF sentence ranking + selection.  
- **Key Files:**  
  - `Summarizer.ipynb` – model training & examples  
  - `requirements.txt`  
- **Outcome:** Summarized text with visualized sentence importance.  
- **Accuracy/Metrics:** Works effectively on arbitrary text; quality depends on input size.  

---

### **Task 2: Multi-Modal Chatbot**

- **Goal:** Extend chatbot to handle text + images using Gemini API.  
- **Features:**  
  - Text conversation  
  - Image insights  
  - AI image generation  
  - Collapsible instruction sidebar  
- **Key Files:**  
  - `app.py` – Streamlit app  
  - `.env` – API key (ignored in repo)  
- **Outcome:** Fully functional multimodal chatbot with UI.  

---

### **Task 3: AI-Powered Knowledge Updater**

- **Goal:** Dynamically expand chatbot knowledge base.  
- **Method:**  
  - Local vector DB (ChromaDB)  
  - Wikipedia fetch + embeddings  
  - Gemini fallback when missing info  
- **Key Files:**  
  - `src/` – embedding, vector store, Gemini bot  
  - `app.py` – Streamlit UI  
- **Outcome:** Chatbot improves knowledge over time.  
- **Accuracy/Metrics:** Vector search + Gemini ensures high recall.  

---

### **Task 4: Sentiment-Aware Chatbot**

- **Goal:** Integrate sentiment analysis into chatbot.  
- **Method:** Logistic Regression + TF-IDF + preprocessing (15k dataset).  
- **Key Files:**  
  - `sentiment_model.ipynb` – training & evaluation  
  - `sentiment_model.pkl` – saved model  
  - `app.py` – Streamlit chatbot  
- **Outcome:** Chatbot adapts replies based on positive/neutral/negative tone.  
- **Accuracy/Metrics:** ~85% accuracy (tested on balanced dataset).  

---

### **Task 5: Research Paper Semantic Search Engine**

- **Goal:** Build expert chatbot for scientific papers (arXiv).  
- **Method:**  
  - Sentence Transformers embeddings  
  - TF-IDF hybrid ranking  
  - Streamlit frontend for search  
- **Key Files:**  
  - `data/arxiv_subset.csv` – dataset  
  - `models/paper_embeddings.npy` – embeddings  
  - `src/search_engine.py` – hybrid ranking  
- **Outcome:** Retrieves and explains relevant research papers.  
- **Accuracy/Metrics:** Returns top-5 most relevant results using cosine similarity.  

---

## ⚙️ Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Pratham-Modi/NullClass_Internship
   cd NullClass_Internship
   ```

2. **Navigate to a Task**  

    Example for Task 2:  

    ```bash
    cd Task2_MultiModalChatbot
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**

    For Jupyter Notebook tasks:

    ```bash
    jupyter notebook Summarizer.ipynb
    ```

    For Streamlit apps:

    ```bash
    streamlit run app.py
    ```

5. **API Keys**

    Create a .env file inside tasks requiring Gemini API:  

    ```bash
    GOOGLE_API_KEY=your_api_key_here
    ```

---

## 📊 Evaluation Metrics (Summary)

- Minimum Accuracy Requirement: 70%
- Task 1: Summarization quality evaluated by coverage of key sentences
- Task 2: Verified text+image integration with Gemini API
- Task 3: Evaluated on ability to add knowledge & fallback to Gemini
- Task 4: Achieved ~85% accuracy (above requirement)
- Task 5: Top-5 paper retrieval accuracy tested with hybrid search

---

## 📌 Final Notes

This repository contains the complete internship deliverables:

- 5 structured tasks, each with its own implementation.
- Streamlit GUIs and Jupyter notebooks where required.
- Achieved required performance metrics
- Fully compliant with company’s submission guidelines.

---

## 👨‍💻 Developed by  

Pratham Modi
