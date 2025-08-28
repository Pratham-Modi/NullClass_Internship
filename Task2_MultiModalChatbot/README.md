# 🤖 Task 2: Multi-Modal Chatbot

This project is an advanced **Multi-Modal Chatbot** that allows users to interact using both **text** and **images**. It provides conversational responses, image analysis, and AI-powered image generation – all in one unified interface.

The entire system is built with an interactive **Streamlit** UI, making it simple and user-friendly.

---

## 🚀 Built With

- 🖥️ `Streamlit` – UI framework for chatbot interaction  
- 🧠 `google-generativeai` – Gemini API for text and vision understanding  
- 🖼️ `PIL` – For handling uploaded images  
- 🔐 `python-dotenv` – For managing API keys securely  

---

## ✨ Features

✅ **💬 Conversation Mode** – Chat with the AI using text prompts  
✅ **🖼️ Image Insight** – Upload an image and ask questions about it  
✅ **🎨 AI Image Generator** – Generate new AI images from text prompts  
✅ **📜 Instruction Sidebar** – Step-by-step guide for using the app  
✅ **📂 Chat History** – Keeps track of your conversation flow  
✅ **🖱️ Collapsible Sidebar** – Toggleable sidebar for instructions & settings  
✅ **🎯 Centered UI Elements** – Clean, modern layout for better user experience  

---

## 🧱 Folder Structure

Task2_MultiModalChatbot/
│
├── app.py              # Streamlit UI and main logic
├── requirements.txt    # Required packages
├── .env                # API key (Git-ignored)
├── .gitignore          # Git ignore for pycache and .env
└── README.md           # Project overview

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Pratham-Modi/NullClass_Internship/tree/main/Task2_MultiModalChatbot
cd NullClassInternship_Task2_MultiModalChatbot
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate  # For Windows
# OR
source venv/bin/activate  # For Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

---

## 💡 Example Usage

### 💬 Chatbot Mode

Ask general questions like:
"Explain black holes in simple terms."

### 🖼️ Image Insight

Upload an image and ask:
"What is in this picture?"

### 🎨 AI Image Generator

Enter a prompt:
"Generate a futuristic city skyline at sunset."

---

## 📦 requirements.txt

```bash
streamlit
Pillow
google-generativeai
python-dotenv
```

---

## 📌 Notes

- Supports text + image multimodal interaction
- Powered by Google Gemini API
- .env is excluded via .gitignore to protect API keys
- Runs locally with no external database setup required

---

## 👨‍💻 Developed by

Pratham Modi  
📅 July 2025
