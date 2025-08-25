import os
import base64
from io import BytesIO
from datetime import datetime
from urllib.parse import quote_plus

import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import requests

# Official Gemini SDK
import google.generativeai as genai

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="✨ Multi-Modal AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# -------------------- ENV & MODEL INIT --------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY not found in .env. Add: GOOGLE_API_KEY=your_key")
    st.stop()

genai.configure(api_key=API_KEY)
MODEL_TEXT_VISION = genai.GenerativeModel("gemini-1.5-flash")

# -------------------- STYLES --------------------
CUSTOM_CSS = """
<style>
.block-container { padding-top: 0.8rem; }
.section-card {
  background: #0b1220;
  border: 1px solid #202a44;
  border-radius: 16px;
  padding: 14px 16px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.30);
}
.chat-pair {
  background: #0f172a;
  border: 1px solid #1f2937;
  border-radius: 14px;
  padding: 10px 12px;
  margin-bottom: 10px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.18);
}
.msg-user {
  background-color: #2563eb;
  color: #ffffff;
  padding: 10px 12px;
  border-radius: 10px;
  margin-bottom: 8px;
}
.msg-bot {
  background-color: #16a34a;
  color: #ffffff;
  padding: 10px 12px;
  border-radius: 10px;
}
.history-box {
  background: #0b1220;
  border: 1px solid #1f2937;
  border-radius: 12px;
  padding: 10px;
  max-height: 360px;
  overflow-y: auto;
}
.small-note { color: #9ca3af; font-size: 12px; margin-top: 6px; text-align: center; }
hr.section-divider { border: none; border-top: 1px dashed #334155; margin: 12px 0; }
.section-heading {
  text-align: center;
  font-size: 1.4rem;
  font-weight: bold;
  margin-bottom: 0.6rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("📘 Instructions")
    st.markdown("""
    Welcome to **NullClass Internship Chatbot** ✨  

    **Features:**
    - 💬 **Conversation:** Ask questions in natural language.
    - 🖼️ **Image Insight:** Upload an image (with or without a prompt).
    - 🎨 **AI Image Generator:** Create images from text prompts.  

    **Tips:**
    - Use the **Clear History** button to reset a section.
    - If Gemini image generation fails, the app uses a free fallback provider.
    - Sidebar can be collapsed with the arrow ⬅️ for more space.
    """)

# -------------------- STATE --------------------
def ensure_states():
    defaults = {
        "conv_history": [],
        "insight_history": [],
        "gen_history": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

ensure_states()

# -------------------- UTILITIES --------------------
def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def b64_to_pil(b64_png: str) -> Image.Image:
    return Image.open(BytesIO(base64.b64decode(b64_png)))

def render_pair(user_text: str, bot_text: str):
    st.markdown('<div class="chat-pair">', unsafe_allow_html=True)
    st.markdown(f'<div class="msg-user"><b>You</b><br>{user_text}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="msg-bot"><b>Bot</b><br>{bot_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_image_pair(img: Image.Image, user_text: str | None, bot_text: str):
    st.markdown('<div class="chat-pair">', unsafe_allow_html=True)
    if user_text:
        st.markdown(f'<div class="msg-user"><b>You</b><br>{user_text}</div>', unsafe_allow_html=True)
    st.image(img, use_container_width=True)
    st.markdown(f'<div class="msg-bot"><b>Bot</b><br>{bot_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_generated(prompt: str, image_src: str, src_type: str):
    st.markdown('<div class="chat-pair">', unsafe_allow_html=True)
    st.markdown(f'<div class="msg-user"><b>You</b><br>{prompt}</div>', unsafe_allow_html=True)
    if src_type == "b64":
        st.image(b64_to_pil(image_src), use_container_width=True)
    else:
        st.image(image_src, use_container_width=True)
    st.markdown(f'<div class="msg-bot"><b>Bot</b><br>Image generated from your prompt.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- CORE (Gemini) --------------------
def generate_text_response(user_text: str) -> str:
    resp = MODEL_TEXT_VISION.generate_content(user_text)
    return (resp.text or "").strip()

def generate_image_description(image_file, prompt: str | None = None) -> str:
    image = Image.open(image_file).convert("RGB")
    parts = [image]
    if prompt and prompt.strip():
        parts.insert(0, prompt.strip())
    else:
        parts.insert(0, "Describe the image in detail: objects, scene, actions, and context.")
    resp = MODEL_TEXT_VISION.generate_content(parts)
    return (resp.text or "").strip()

def try_gemini_image(prompt: str) -> str:
    resp = MODEL_TEXT_VISION.generate_content(
        prompt,
        generation_config={"response_mime_type": "image/png"}
    )
    if hasattr(resp, "candidates") and resp.candidates:
        parts = resp.candidates[0].content.parts
        for p in parts:
            inline = getattr(p, "inline_data", None)
            if inline and getattr(inline, "mime_type", "") == "image/png" and getattr(inline, "data", None):
                return inline.data
            if getattr(p, "mime_type", "") == "image/png" and getattr(p, "data", None):
                return p.data
    raise RuntimeError("Gemini did not return image bytes.")

def pollinations_url(prompt: str, width: int = 768, height: int = 512) -> str:
    safe = quote_plus(prompt)
    return f"https://image.pollinations.ai/prompt/{safe}?width={width}&height={height}"

# -------------------- HEADER --------------------
st.markdown("<h1 style='text-align:center;'>🤖✨ Multi-Modal AI Chatbot</h1>", unsafe_allow_html=True)
st.markdown('<div class="small-note">Chat • Image Insight • Image Generation — all in one app</div>', unsafe_allow_html=True)
st.markdown('<hr class="section-divider" />', unsafe_allow_html=True)

# -------------------- TAB SECTIONS --------------------
tab1, tab2, tab3 = st.tabs(["💬 Conversation", "🖼️ Image Insight", "🎨 AI Image Generator"])

# =========================================================
# 💬 Conversation (Text → Text)
# =========================================================
with tab1:
    st.markdown('<div class="section-heading">💬 Conversation</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    msg = st.text_input("Message", key="conv_input", placeholder="Ask anything...")
    if st.button("Send", key="conv_send"):
        if msg and msg.strip():
            try:
                ans = generate_text_response(msg.strip())
            except Exception as e:
                ans = f"Error: {e}"
            st.session_state.conv_history.append({"q": msg.strip(), "a": ans, "ts": ts()})
        else:
            st.warning("Please type a message.")

    st.markdown("**History**")
    st.markdown('<div class="history-box">', unsafe_allow_html=True)
    for item in reversed(st.session_state.conv_history):
        render_pair(item["q"], item["a"])
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Clear History", key="conv_clear"):
        st.session_state.conv_history = []

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 🖼️ Image Insight (Image [+ Optional Prompt] → Text)
# =========================================================
with tab2:
    st.markdown('<div class="section-heading">🖼️ Image Insight</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    up = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="insight_up")
    prompt_insight = st.text_input("Optional prompt (e.g., “Focus on the person’s activity”)", key="insight_prompt")

    if up is not None:
        try:
            preview = Image.open(up).convert("RGB")
            st.image(preview, caption="Preview", use_container_width=True)
            up.seek(0)
        except Exception:
            st.warning("Could not preview this image, but analysis may still work.")

    if st.button("Analyze", key="insight_btn"):
        if up is None:
            st.warning("Please upload an image first.")
        else:
            raw_bytes = up.getvalue()
            try:
                insight = generate_image_description(BytesIO(raw_bytes), prompt_insight.strip() if prompt_insight else None)
                st.session_state.insight_history.append({
                    "prompt": (prompt_insight.strip() if prompt_insight else None),
                    "image_bytes": raw_bytes,
                    "a": insight,
                    "ts": ts()
                })
            except Exception as e:
                st.error(f"Analysis failed: {e}")

    st.markdown("**History**")
    st.markdown('<div class="history-box">', unsafe_allow_html=True)
    for item in reversed(st.session_state.insight_history):
        try:
            img = Image.open(BytesIO(item["image_bytes"]))
        except Exception:
            img = Image.new("RGB", (512, 320), color=(32, 32, 32))
        render_image_pair(img, item["prompt"], item["a"])
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Clear History", key="insight_clear"):
        st.session_state.insight_history = []

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 🎨 AI Image Generator (Text → Image)
# =========================================================
with tab3:
    st.markdown('<div class="section-heading">🎨 AI Image Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    gen_prompt = st.text_area("Prompt", key="gen_prompt", placeholder="e.g., “A neon cyberpunk city at night, isometric, highly detailed”")
    if st.button("Generate", key="gen_btn"):
        if gen_prompt and gen_prompt.strip():
            try:
                b64_png = try_gemini_image(gen_prompt.strip())
                st.session_state.gen_history.append({
                    "prompt": gen_prompt.strip(),
                    "image_src": b64_png,
                    "src_type": "b64",
                    "ts": ts()
                })
            except Exception:
                url = pollinations_url(gen_prompt.strip())
                try:
                    _ = requests.get(url, timeout=20)
                except Exception:
                    pass
                st.session_state.gen_history.append({
                    "prompt": gen_prompt.strip(),
                    "image_src": url,
                    "src_type": "url",
                    "ts": ts()
                })
        else:
            st.warning("Please enter a prompt to generate an image.")

    st.markdown("**Generation History**")
    st.markdown('<div class="history-box">', unsafe_allow_html=True)
    for item in reversed(st.session_state.gen_history):
        render_generated(item["prompt"], item["image_src"], item["src_type"])
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Clear History", key="gen_clear"):
        st.session_state.gen_history = []

    st.markdown('<div class="small-note">If Gemini image generation isn’t available on your account, the app uses a free fallback provider automatically.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.markdown('<hr class="section-divider" />', unsafe_allow_html=True)
st.markdown('<div class="small-note">Built with Gemini 1.5 Flash • Fully local UI • Free text-to-image fallback</div>', unsafe_allow_html=True)
