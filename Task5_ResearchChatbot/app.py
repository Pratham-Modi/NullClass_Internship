import streamlit as st
from src.search_engine import PaperSearchEngine

st.set_page_config(
    page_title="Research Paper Search Chatbot",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar info
with st.sidebar:
    st.header("🔍 About")
    st.write(
        """
        This app helps you find relevant academic papers using semantic search powered by SentenceTransformer embeddings.
        Enter your research keywords or questions below and get the top matching papers with abstracts.
        """
    )
    st.markdown("---")
    st.header("Tips")
    st.write(
        """
        - Use clear and concise queries.
        - Try different keyword combinations for better results.
        - Scroll through results for more insights.
        """
    )

@st.cache_data(show_spinner=True)
def load_search_engine():
    embeddings_path = "models/paper_embeddings.npy"
    csv_path = "data/arxiv_subset.csv"
    return PaperSearchEngine(embeddings_path, csv_path, alpha=0.6)  # You can tune alpha here

search_engine = load_search_engine()

st.title("🔍 Research Paper Search Chatbot")
st.markdown(
    """
    Enter your research query below to find the most relevant academic papers.
    Powered by semantic search using SentenceTransformer embeddings.
    """
)

with st.form("search_form"):
    query = st.text_input("Enter keywords or question", max_chars=150, placeholder="E.g., machine learning applications in healthcare")
    submitted = st.form_submit_button("Search")

if submitted and query.strip():
    with st.spinner("Searching for relevant papers..."):
        results = search_engine.search(query.strip(), top_k=5)

    if results:
        st.success(f"Found {len(results)} relevant papers:")
        for i, paper in enumerate(results, start=1):
            st.markdown(f"### {i}. {paper['title']}")
            authors = paper.get('authors', 'N/A')
            st.markdown(f"**Authors:** {authors}")
            st.write(paper['abstract'])
            st.markdown(f"**Relevance Score:** {paper['score']:.4f}")
            st.markdown("---")
    else:
        st.warning("No relevant papers found. Try refining your query.")
else:
    st.info("Please enter a query to start searching.")
