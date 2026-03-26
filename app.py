import re
import unicodedata
import joblib
import streamlit as st
from pathlib import Path
from attacut import tokenize


# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Shopping Review Classifier",
    page_icon="🛍️",
    layout="centered"
)

# =========================
# Custom CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 60% at 50% -20%, rgba(120, 80, 255, 0.18) 0%, transparent 70%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(255, 80, 120, 0.10) 0%, transparent 60%);
    min-height: 100vh;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 720px; }

/* ── Hero Header ── */
.hero-wrapper {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #a78bfa;
    background: rgba(167, 139, 250, 0.12);
    border: 1px solid rgba(167, 139, 250, 0.25);
    padding: 0.3rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    margin: 0.2rem 0 0.8rem;
    letter-spacing: -0.03em;
}
.hero-title span {
    background: linear-gradient(135deg, #c084fc 0%, #f472b6 60%, #fb923c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 0.95rem;
    font-weight: 300;
    color: rgba(255,255,255,0.45);
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.4), rgba(244,114,182,0.4), transparent);
    margin: 2rem 0;
}

/* ── Input Card ── */
.input-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1rem;
}
.input-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.55);
    margin-bottom: 0.6rem;
}

/* ── Streamlit textarea override ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.06) !important;
    border: 1.5px solid rgba(167,139,250,0.25) !important;
    border-radius: 12px !important;
    color: #f0e6ff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.65 !important;
    padding: 0.9rem 1rem !important;
    transition: border-color 0.2s ease !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: rgba(192,132,252,0.7) !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.12) !important;
}
.stTextArea textarea::placeholder { color: rgba(255,255,255,0.25) !important; }
.stTextArea label { display: none !important; }

/* ── Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 24px rgba(124,58,237,0.35) !important;
    margin-top: 0.8rem !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(124,58,237,0.5) !important;
    filter: brightness(1.1) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Result Cards ── */
.result-pos {
    background: linear-gradient(135deg, rgba(16,185,129,0.15) 0%, rgba(5,150,105,0.08) 100%);
    border: 1.5px solid rgba(16,185,129,0.35);
    border-radius: 16px;
    padding: 1.8rem;
    margin: 1.2rem 0;
    position: relative;
    overflow: hidden;
}
.result-pos::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #10b981, #34d399);
    border-radius: 16px 16px 0 0;
}
.result-neg {
    background: linear-gradient(135deg, rgba(239,68,68,0.15) 0%, rgba(185,28,28,0.08) 100%);
    border: 1.5px solid rgba(239,68,68,0.35);
    border-radius: 16px;
    padding: 1.8rem;
    margin: 1.2rem 0;
    position: relative;
    overflow: hidden;
}
.result-neg::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #ef4444, #f87171);
    border-radius: 16px 16px 0 0;
}
.result-icon {
    font-size: 2.8rem;
    line-height: 1;
    margin-bottom: 0.5rem;
}
.result-label-en {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 0.15rem;
}
.result-pos .result-label-en { color: #34d399; }
.result-neg .result-label-en { color: #f87171; }
.result-label-th {
    font-size: 1rem;
    font-weight: 400;
    opacity: 0.75;
    color: #e0e0e0;
}

/* ── Process Steps ── */
.process-section {
    margin-top: 1.8rem;
}
.process-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.35);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.process-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.08);
}
.process-step {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
    position: relative;
    padding-left: 1.4rem;
}
.step-num {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(167,139,250,0.6);
    margin-bottom: 0.25rem;
}
.step-text {
    font-size: 0.9rem;
    color: rgba(255,255,255,0.7);
    line-height: 1.6;
    word-break: break-word;
    font-family: 'DM Mono', 'Courier New', monospace;
}
.step-text.original {
    font-family: 'DM Sans', sans-serif;
    color: rgba(255,255,255,0.85);
    font-size: 0.95rem;
}

/* ── Warning / Error ── */
.stAlert {
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Footer ── */
.custom-footer {
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.07);
}
.footer-model-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.3);
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.04em;
}
.footer-dot {
    width: 4px; height: 4px;
    border-radius: 50%;
    background: rgba(167,139,250,0.5);
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Load Model
# =========================
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "best_review_model.pkl"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()


# =========================
# Text Preprocessing
# =========================
def clean_text_thai(text):
    text = str(text)
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'[@#]\S+', ' ', text)
    text = re.sub(r'[\n\r\t]', ' ', text)
    text = re.sub(r'[\u200b-\u200d\uFEFF]', '', text)
    text = re.sub(r'([ก-๙a-zA-Z])\1{2,}', r'\1\1', text)
    text = re.sub(r'([!?.,])\1{1,}', r'\1', text)
    text = re.sub(r'[^ก-๙a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_text(text):
    tokens = tokenize(text)
    return " ".join(tokens)

def preprocess_for_model(text):
    cleaned = clean_text_thai(text)
    tokenized = tokenize_text(cleaned)
    return cleaned, tokenized

# =========================
# Label Mapping
# =========================
def map_prediction_label(pred):
    if pred == "pos":
        return "Positive", "รีวิวเชิงบวก", "😊"
    elif pred == "neg":
        return "Negative", "รีวิวเชิงลบ", "😞"
    else:
        return pred, f"Prediction: {pred}", "🤔"

# =========================
# UI — Hero
# =========================
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-badge">🛍️ &nbsp;Sentiment Analysis · Thai NLP</div>
    <div class="hero-title">Shopping Review<br><span>Classifier</span></div>
    <div class="hero-subtitle">วิเคราะห์ความรู้สึกรีวิวสินค้าภาษาไทย ด้วย TF-IDF + Logistic Regression</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# =========================
# Input Area
# =========================
st.markdown("""
<div class="input-card">
    <div class="input-label">📝 &nbsp;ข้อความรีวิว</div>
</div>
""", unsafe_allow_html=True)

user_input = st.text_area(
    label="review_input",
    height=140,
    placeholder="พิมพ์รีวิวสินค้าที่นี่  เช่น  สินค้าดีมาก ส่งเร็ว แพ็คของดี ประทับใจมาก 😍",
    label_visibility="collapsed"
)

predict_button = st.button("🔍  วิเคราะห์ความรู้สึก")

# =========================
# Prediction
# =========================
if predict_button:
    if not user_input.strip():
        st.warning("⚠️  กรุณากรอกข้อความรีวิวก่อนกดวิเคราะห์")
    else:
        cleaned_text, tokenized_text = preprocess_for_model(user_input)

        if tokenized_text.strip() == "":
            st.error("❌  ข้อความหลัง preprocessing ว่างเปล่า ไม่สามารถทำนายได้")
        else:
            with st.spinner("กำลังวิเคราะห์..."):
                prediction = model.predict([tokenized_text])[0]

            label_en, label_th, icon = map_prediction_label(prediction)

            css_class = "result-pos" if prediction == "pos" else "result-neg"

            st.markdown(f"""
<div class="{css_class}">
    <div class="result-icon">{icon}</div>
    <div class="result-label-en">{label_en}</div>
    <div class="result-label-th">{label_th}</div>
</div>
""", unsafe_allow_html=True)

            # ── Processing Details ──
            st.markdown("""
<div class="process-section">
    <div class="process-title">ขั้นตอนการประมวลผล</div>
</div>
""", unsafe_allow_html=True)

            st.markdown(f"""
<div class="process-step">
    <div class="step-num">① Original Text</div>
    <div class="step-text original">{user_input}</div>
</div>
<div class="process-step">
    <div class="step-num">② Cleaned Text</div>
    <div class="step-text">{cleaned_text}</div>
</div>
<div class="process-step">
    <div class="step-num">③ Tokenized Text</div>
    <div class="step-text">{tokenized_text}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.markdown("""
<div class="custom-footer">
    <div class="footer-model-badge">
        Built with Streamlit
        <span class="footer-dot"></span>
        TF-IDF + Logistic Regression
        <span class="footer-dot"></span>
        AttaCut Tokenizer
    </div>
</div>
""", unsafe_allow_html=True)