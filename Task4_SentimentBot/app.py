import streamlit as st
from src.sentiment_logic import analyze_sentiment

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="Sentiment Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Sentiment-Aware Chatbot")
st.write("Type a message and I'll detect its sentiment!")

# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Custom colors for sentiment
SENTIMENT_COLORS = {
    "POSITIVE": "#4CAF50",
    "NEGATIVE": "#F44336",
    "NEUTRAL": "#FFC107",
    "DEFAULT": "#2196F3"
}

def styled_message(sender, text, sentiment="DEFAULT"):
    color = SENTIMENT_COLORS.get(sentiment, SENTIMENT_COLORS["DEFAULT"])
    st.markdown(
        f"""
        <div style="
            background-color: {color};
            padding: 10px 15px;
            border-radius: 10px;
            margin: 5px 0;
            color: white;
            font-weight: 500;
        ">
            <b>{sender}:</b> {text}
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Message Processing Function
# -----------------------------
def process_message(text):
    sentiment_result = analyze_sentiment(text)
    sentiment = sentiment_result["label"]

    if sentiment == "POSITIVE":
        bot_reply = "😊 I'm glad to hear that!"
    elif sentiment == "NEGATIVE":
        bot_reply = "😔 I'm sorry to hear that. Do you want to talk more about it?"
    else:
        bot_reply = "😐 Got it. Thanks for sharing!"

    st.session_state.messages.append(("You", text, "DEFAULT"))
    st.session_state.messages.append(("Bot", f"{bot_reply} (Detected: {sentiment})", sentiment))

# -----------------------------
# User Input with Enter Key Support
# -----------------------------
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

def on_enter():
    text = st.session_state.input_text.strip()
    if text:
        process_message(text)
        st.session_state.input_text = ""  # Reset input

user_input = st.text_input(
    "You:",
    st.session_state.input_text,
    key="input_text",
    on_change=on_enter
)

# -----------------------------
# Buttons
# -----------------------------
col1, col2 = st.columns([3, 1])
with col1:
    if st.button("Analyze sentiment", key="analyze_btn") and st.session_state.input_text.strip():
        on_enter()

with col2:
    if st.button("Clear History", key="clear_btn"):
        st.session_state.messages = []

# -----------------------------
# Display Conversation
# -----------------------------
for sender, msg, senti in st.session_state.messages:
    styled_message(sender, msg, senti)

