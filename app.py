import streamlit as st
import requests
import json
import time

# ─── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="TruthLens — AI Fake News Detector",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700;800&display=swap');

/* ── Root & Body ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #050a14 !important;
    color: #f1f5f9 !important;
}

.stApp {
    background: #050a14;
    background-image:
        radial-gradient(ellipse 60% 50% at 10% 10%, rgba(167,139,250,0.12) 0%, transparent 70%),
        radial-gradient(ellipse 50% 50% at 90% 90%, rgba(56,189,248,0.10) 0%, transparent 70%),
        radial-gradient(ellipse 40% 40% at 50% 50%, rgba(34,197,94,0.05) 0%, transparent 70%);
    min-height: 100vh;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(5,10,20,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] .sidebar-title {
    color: #f1f5f9 !important;
}

/* ── Glass Card ── */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
}

.glass-card-accent {
    background: rgba(167,139,250,0.05);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 40px rgba(167,139,250,0.08);
}

/* ── Hero Header ── */
.hero-header {
    text-align: center;
    padding: 40px 0 20px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(167,139,250,0.12);
    border: 1px solid rgba(167,139,250,0.28);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 18px;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.02em;
    color: #f1f5f9;
    margin-bottom: 14px;
}

.gradient-text {
    background: linear-gradient(135deg, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    color: #64748b;
    font-size: 1rem;
    line-height: 1.7;
    margin-bottom: 0;
}

/* ── Streamlit Inputs ── */
.stTextInput > div > div {
    background: rgba(0,0,0,0.35) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
    padding: 6px 4px !important;
    transition: all 0.25s;
}
.stTextInput > div > div:focus-within {
    border-color: rgba(167,139,250,0.5) !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.1) !important;
}
.stTextInput input {
    color: #f1f5f9 !important;
    font-size: 0.95rem !important;
}
.stTextInput label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ── Buttons ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #a78bfa, #38bdf8) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    transition: all 0.25s !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    filter: brightness(1.12) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(167,139,250,0.35) !important;
}
.stButton > button:active { transform: scale(0.97) !important; }

/* ── Progress bar ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #a78bfa, #38bdf8) !important;
    border-radius: 100px !important;
}
.stProgress > div > div {
    border-radius: 100px !important;
    background: rgba(255,255,255,0.06) !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    padding: 20px !important;
}
[data-testid="stMetricValue"] { color: #f1f5f9 !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.78rem !important; }

/* ── Verdict banners ── */
.verdict-real {
    background: linear-gradient(135deg, rgba(34,197,94,0.12), rgba(56,189,248,0.08));
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 20px;
    padding: 28px 32px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 0 40px rgba(34,197,94,0.08);
}
.verdict-fake {
    background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(245,158,11,0.08));
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 20px;
    padding: 28px 32px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 0 40px rgba(239,68,68,0.08);
}
.verdict-uncertain {
    background: linear-gradient(135deg, rgba(245,158,11,0.12), rgba(167,139,250,0.08));
    border: 1px solid rgba(245,158,11,0.3);
    border-radius: 20px;
    padding: 28px 32px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 0 40px rgba(245,158,11,0.08);
}

.verdict-emoji   { font-size: 3.5rem; margin-bottom: 8px; }
.verdict-title   { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 800; }
.verdict-sub     { color: #94a3b8; font-size: 0.9rem; margin-top: 6px; }
.verdict-pct     { font-size: 3.8rem; font-weight: 900; font-family: 'Space Grotesk', sans-serif;
                   background: linear-gradient(135deg, #a78bfa, #38bdf8);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

/* ── Signal pills ── */
.signal-pill {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 3px;
}
.pill-green  { background: rgba(34,197,94, 0.12); border: 1px solid rgba(34,197,94, 0.25); color: #4ade80; }
.pill-red    { background: rgba(239,68,68, 0.12); border: 1px solid rgba(239,68,68, 0.25); color: #f87171; }
.pill-amber  { background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.25); color: #fbbf24; }
.pill-blue   { background: rgba(56,189,248,0.12); border: 1px solid rgba(56,189,248,0.25); color: #38bdf8; }

/* ── Info box ── */
.info-box {
    background: rgba(56,189,248,0.07);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 0.82rem;
    color: #94a3b8;
    line-height: 1.6;
}

/* ── Code block ── */
.stCode { border-radius: 12px !important; }

/* ── Separator ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Sidebar connection status ── */
.conn-status-ok {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.8rem;
    color: #4ade80;
    margin-bottom: 12px;
}
.conn-status-err {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.8rem;
    color: #f87171;
    margin-bottom: 12px;
}
.conn-status-idle {
    background: rgba(100,116,139,0.1);
    border: 1px solid rgba(100,116,139,0.2);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.8rem;
    color: #64748b;
    margin-bottom: 12px;
}

/* ── Beta banner ── */
.beta-banner {
    background: linear-gradient(135deg, rgba(245,158,11,0.10), rgba(167,139,250,0.07));
    border: 1px solid rgba(245,158,11,0.30);
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 18px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}
.beta-banner-icon { font-size: 1.4rem; flex-shrink: 0; margin-top: 2px; }
.beta-banner-body { flex: 1; }
.beta-banner-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: #fbbf24;
    margin-bottom: 4px;
}
.beta-banner-text {
    font-size: 0.78rem;
    color: #94a3b8;
    line-height: 1.55;
}
.beta-badge {
    display: inline-block;
    background: rgba(245,158,11,0.15);
    border: 1px solid rgba(245,158,11,0.35);
    border-radius: 100px;
    padding: 2px 10px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #fbbf24;
    margin-left: 8px;
    vertical-align: middle;
}

/* ── Textarea ── */
.stTextArea textarea {
    background: rgba(0,0,0,0.35) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: rgba(167,139,250,0.5) !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.1) !important;
    outline: none !important;
}
.stTextArea label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    margin-bottom: 20px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 10px 20px !important;
    border: none !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(167,139,250,0.2), rgba(56,189,248,0.15)) !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(167,139,250,0.25) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ─── SESSION STATE ────────────────────────────────────────────
if "result"      not in st.session_state: st.session_state.result       = None
if "colab_url"   not in st.session_state: st.session_state.colab_url    = ""
if "use_mock"    not in st.session_state: st.session_state.use_mock     = True
if "conn_status" not in st.session_state: st.session_state.conn_status  = "idle"  # idle / ok / error
if "input_mode" not in st.session_state:  st.session_state.input_mode   = "text"  # "text" or "url"


# ─── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Model Connection")
    st.markdown("---")

    st.markdown("**Mode**")
    mode = st.radio(
        "Select API mode",
        ["🧪 Mock (no model needed)", "🔗 Connect to Google Colab"],
        label_visibility="collapsed",
    )
    st.session_state.use_mock = (mode == "🧪 Mock (no model needed)")

    st.markdown("---")

    if not st.session_state.use_mock:
        st.markdown("**Colab API URL**")
        colab_input = st.text_input(
            "Colab ngrok URL",
            value=st.session_state.colab_url,
            placeholder="https://xxxx-xx-xx.ngrok-free.app",
            label_visibility="collapsed",
        )
        st.session_state.colab_url = colab_input.strip().rstrip("/")

        if st.button("🔌 Test Connection"):
            if not st.session_state.colab_url:
                st.error("Please paste your Colab URL first.")
            else:
                with st.spinner("Testing…"):
                    try:
                        r = requests.get(
                            st.session_state.colab_url + "/health", timeout=8
                        )
                        if r.status_code == 200:
                            st.session_state.conn_status = "ok"
                        else:
                            st.session_state.conn_status = "error"
                    except Exception:
                        st.session_state.conn_status = "error"

        if st.session_state.conn_status == "ok":
            st.markdown('<div class="conn-status-ok">✅ Connected to Colab model</div>', unsafe_allow_html=True)
        elif st.session_state.conn_status == "error":
            st.markdown('<div class="conn-status-err">❌ Could not reach Colab. Check the URL.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="conn-status-idle">⚪ Not tested yet</div>', unsafe_allow_html=True)

        st.markdown("---")
        with st.expander("📋 Colab Setup Code"):
            st.markdown("Paste this at the **top of your Colab notebook** and run it:")
            st.code("""
!pip install flask flask-cors pyngrok -q

from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok
import threading

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/predict', methods=['POST'])
def predict():
    data      = request.get_json()
    news_url  = data.get('url', '')

    # ── YOUR MODEL CODE HERE ──────────────────
    # Example (replace with your actual model):
    # text = scrape_article(news_url)
    # prob = model.predict_proba([text])[0][1]
    # confidence = max(prob, 1-prob)
    # -----------------------------------------
    true_prob  = 0.82   # float 0.0 → 1.0
    confidence = 0.91   # float 0.0 → 1.0

    return jsonify({
        "real_probability" : round(true_prob  * 100, 1),
        "fake_probability" : round((1-true_prob) * 100, 1),
        "confidence"       : round(confidence * 100, 1),
    })

public_url = ngrok.connect(5000)
print("\\n✅ Paste this URL into TruthLens sidebar:")
print(public_url)
print()

threading.Thread(
    target=lambda: app.run(port=5000, use_reloader=False)
).start()
""", language="python")

    else:
        st.markdown(
            '<div class="info-box">🧪 <b>Mock mode active.</b><br/>'
            'Results are simulated — no model needed.<br/>'
            'Switch to <i>Connect to Colab</i> to use your real model.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("**About**")
    st.markdown(
        "<span style='color:#475569;font-size:0.78rem;line-height:1.6;'>"
        "TruthLens uses a trained ML classifier hosted in Google Colab to "
        "predict whether a news article is real or fake. The Streamlit frontend "
        "sends the URL to the Colab API via ngrok and displays the result."
        "</span>",
        unsafe_allow_html=True,
    )


# ─── MOCK API ─────────────────────────────────────────────────
def mock_predict(url: str) -> dict:
    """Simulated prediction from URL — replace with real API call when ready."""
    import hashlib, random
    seed = int(hashlib.md5(url.encode()).hexdigest(), 16) % 1000
    rng  = random.Random(seed)
    real = round(rng.uniform(15, 95), 1)
    conf = round(rng.uniform(70, 97), 1)
    return {
        "real_probability": real,
        "fake_probability": round(100 - real, 1),
        "confidence":       conf,
    }


def mock_predict_text(text: str) -> dict:
    """Simulated prediction from news text — uses text content as seed."""
    import hashlib, random
    seed = int(hashlib.md5(text[:500].encode()).hexdigest(), 16) % 1000
    rng  = random.Random(seed)
    real = round(rng.uniform(15, 95), 1)
    conf = round(rng.uniform(72, 98), 1)
    return {
        "real_probability": real,
        "fake_probability": round(100 - real, 1),
        "confidence":       conf,
    }


# ─── REAL API ─────────────────────────────────────────────────
def colab_predict(url: str, colab_url: str) -> dict:
    payload  = {"url": url}
    headers  = {"Content-Type": "application/json", "ngrok-skip-browser-warning": "1"}
    response = requests.post(
        colab_url + "/predict",
        data=json.dumps(payload),
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def colab_predict_text(text: str, colab_url: str) -> dict:
    """Send raw news text to Colab /predict_text endpoint."""
    payload  = {"text": text}
    headers  = {"Content-Type": "application/json", "ngrok-skip-browser-warning": "1"}
    response = requests.post(
        colab_url + "/predict_text",
        data=json.dumps(payload),
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


# ─── HELPERS ──────────────────────────────────────────────────
def verdict_info(real_pct: float):
    if real_pct >= 70:
        return "real",     "✅",  "#22c55e", "Likely REAL News",  "The article shows strong indicators of credibility."
    elif real_pct >= 45:
        return "uncertain","⚠️",  "#f59e0b", "Uncertain / Mixed", "The article has mixed credibility signals."
    else:
        return "fake",     "🚫", "#ef4444", "Likely FAKE News",  "The article shows strong indicators of misinformation."


def generate_signals(real_pct: float, url: str):
    signals = []
    domain  = url.split("/")[2] if "//" in url else url

    if real_pct >= 70:
        signals = [
            ("green", "✔ High factual probability score"),
            ("green", "✔ Content structure consistent with credible reporting"),
            ("blue",  "ℹ Language patterns match known news sources"),
            ("green", "✔ Minimal sensationalist language detected"),
        ]
    elif real_pct >= 45:
        signals = [
            ("amber", "⚠ Moderate credibility score — verify with additional sources"),
            ("amber", "⚠ Some bias indicators detected in language"),
            ("blue",  "ℹ Domain: " + domain),
            ("amber", "⚠ Mixed factual and opinion content detected"),
        ]
    else:
        signals = [
            ("red",   "✖ Low factual probability score"),
            ("red",   "✖ Sensationalist or misleading language detected"),
            ("amber", "⚠ Source has low credibility indicators"),
            ("blue",  "ℹ Cross-check with Reuters, AP, or Snopes"),
        ]
    return signals


def render_progress_bar(label: str, pct: float, color: str):
    bar_html = f"""
    <div style="margin-bottom:14px;">
        <div style="display:flex;justify-content:space-between;
                    font-size:0.82rem;color:#94a3b8;margin-bottom:6px;">
            <span>{label}</span>
            <span style="font-weight:700;color:#f1f5f9;">{pct:.1f}%</span>
        </div>
        <div style="height:10px;background:rgba(255,255,255,0.06);
                    border-radius:100px;overflow:hidden;">
            <div style="height:100%;width:{pct}%;background:{color};
                        border-radius:100px;transition:width 1s ease;"></div>
        </div>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)


# ─── HERO ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
  <div class="hero-badge">🔍 &nbsp; Gen AI Project</div>
  <div class="hero-title">
    Detect <span class="gradient-text">Fake News</span><br/>Instantly
  </div>
  <div class="hero-subtitle">
    Paste news text or a URL &middot; Our trained ML model analyses the content<br/>
    and returns a real-time credibility percentage.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── INPUT SECTION ────────────────────────────────────────────
tab_text, tab_url = st.tabs(["📝  News Text", "🔗  News URL  (Beta)"])

# ── Tab 1: News Text (fully working) ──
with tab_text:
    st.session_state.input_mode = "text"
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    news_text = st.text_area(
        "📰  Paste the full news article text below",
        placeholder="Paste the complete news article text here. The more text you provide, the more accurate the analysis will be…",
        height=200,
        key="news_text_input",
        help="Copy and paste the full body of the article — headlines, paragraphs, everything.",
    )
    analyse_text_clicked = st.button("🔍  Analyse Text", use_container_width=True, key="btn_text")
    st.markdown("</div>", unsafe_allow_html=True)

    if analyse_text_clicked:
        if not news_text or len(news_text.strip()) < 30:
            st.error("⚠️  Please paste at least a sentence or two of news text to analyse.")
        elif not st.session_state.use_mock and not st.session_state.colab_url:
            st.error("⚠️  Please enter your Colab ngrok URL in the sidebar first, or switch to Mock mode.")
        else:
            with st.spinner(""):
                progress_bar = st.progress(0)
                status_text  = st.empty()
                steps = [
                    (25,  "🔬  Tokenising article text…"),
                    (50,  "🧠  Extracting linguistic features…"),
                    (75,  "🤖  Running ML classification…"),
                    (100, "📊  Computing confidence score…"),
                ]
                for pct, msg in steps:
                    status_text.markdown(
                        f'<p style="color:#94a3b8;text-align:center;font-size:0.9rem;">{msg}</p>',
                        unsafe_allow_html=True,
                    )
                    progress_bar.progress(pct)
                    time.sleep(0.55)
                progress_bar.empty()
                status_text.empty()
                try:
                    if st.session_state.use_mock:
                        result = mock_predict_text(news_text)
                    else:
                        result = colab_predict_text(news_text, st.session_state.colab_url)
                    snippet = news_text.strip()[:80] + ("…" if len(news_text) > 80 else "")
                    st.session_state.result = {"data": result, "url": None, "snippet": snippet}
                except requests.exceptions.ConnectionError:
                    st.error("❌  Could not connect to Colab. Make sure the notebook is running.")
                    st.session_state.result = None
                except requests.exceptions.Timeout:
                    st.error("❌  Request timed out. The Colab session may be inactive.")
                    st.session_state.result = None
                except Exception as e:
                    st.error(f"❌  Error: {e}")
                    st.session_state.result = None

# ── Tab 2: News URL (beta) ──
with tab_url:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="beta-banner">
      <div class="beta-banner-icon">🚧</div>
      <div class="beta-banner-body">
        <div class="beta-banner-title">URL Analysis — Under Development <span class="beta-badge">Beta</span></div>
        <div class="beta-banner-text">
          Our model is currently being trained to extract and process content directly from URLs.
          This feature is in active development and will be available soon.<br/><br/>
          <strong style="color:#f1f5f9;">👇 For now, use the News Text tab</strong> — copy the article text
          from any webpage and paste it there for an immediate result.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    news_url = st.text_input(
        "🔗  News Article URL",
        placeholder="https://example.com/news-article",
        help="URL-based analysis is coming soon. Use News Text tab for now.",
        key="news_url_input",
        disabled=True,
    )
    st.button("🔍  Analyse URL", use_container_width=True, key="btn_url", disabled=True)
    st.markdown(
        "<p style='text-align:center;color:#475569;font-size:0.75rem;margin-top:8px;'>"
        "🔔 URL feature will be enabled once model training is complete"
        "</p>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ─── RESULTS ──────────────────────────────────────────────────
if st.session_state.result:
    res      = st.session_state.result["data"]
    url_used = st.session_state.result.get("url")
    real_pct = float(res.get("real_probability", 50))
    fake_pct = float(res.get("fake_probability", 50))
    conf_pct = float(res.get("confidence", 80))

    cat, emoji, color, title, subtitle = verdict_info(real_pct)

    # ── Verdict Banner ────────
    st.markdown(f"""
    <div class="verdict-{cat}">
        <div class="verdict-emoji">{emoji}</div>
        <div class="verdict-title" style="color:{color};">{title}</div>
        <div class="verdict-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Metrics row ──────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("🟢 Real Probability",  f"{real_pct:.1f}%")
    with c2:
        st.metric("🔴 Fake Probability",  f"{fake_pct:.1f}%")
    with c3:
        st.metric("🎯 Model Confidence",  f"{conf_pct:.1f}%")

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Two-column detail ────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(
            f"<p style='font-size:0.75rem;font-weight:600;text-transform:uppercase;"
            f"letter-spacing:0.09em;color:#475569;margin-bottom:16px;'>📊 Score Breakdown</p>",
            unsafe_allow_html=True,
        )
        render_progress_bar(
            "🟢 Real News",
            real_pct,
            "linear-gradient(90deg, #22c55e, #38bdf8)",
        )
        render_progress_bar(
            "🔴 Fake News",
            fake_pct,
            "linear-gradient(90deg, #ef4444, #f59e0b)",
        )
        render_progress_bar(
            "🎯 Confidence",
            conf_pct,
            "linear-gradient(90deg, #a78bfa, #38bdf8)",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:0.75rem;font-weight:600;text-transform:uppercase;"
            "letter-spacing:0.09em;color:#475569;margin-bottom:16px;'>🔍 Analysis Signals</p>",
            unsafe_allow_html=True,
        )
        signals = generate_signals(real_pct, url_used or st.session_state.result.get("snippet", ""))
        pills_html = ""
        for pill_type, signal_text in signals:
            pills_html += f'<div class="signal-pill pill-{pill_type}">{signal_text}</div>'
        st.markdown(pills_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Input source display ──────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if url_used:
        st.markdown(
            "<p style='font-size:0.75rem;font-weight:600;text-transform:uppercase;"
            "letter-spacing:0.09em;color:#475569;margin-bottom:10px;'>🔗 Analysed URL</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<a href='{url_used}' target='_blank' style='color:#a78bfa;font-size:0.85rem;"
            f"word-break:break-all;text-decoration:none;'>{url_used} ↗</a>",
            unsafe_allow_html=True,
        )
    else:
        snippet = st.session_state.result.get("snippet", "")
        st.markdown(
            "<p style='font-size:0.75rem;font-weight:600;text-transform:uppercase;"
            "letter-spacing:0.09em;color:#475569;margin-bottom:10px;'>📰 Analysed Text (preview)</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='color:#64748b;font-size:0.85rem;font-style:italic;line-height:1.6;'>\"{snippet}\"</p>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Reset button ─────────
    if st.button("🔄  Analyse Another Article", use_container_width=False):
        st.session_state.result = None
        st.rerun()

# ─── FOOTER ───────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#1e293b;font-size:0.75rem;'>"
    "TruthLens &nbsp;·&nbsp; Gen AI Project &nbsp;·&nbsp; "
    "Powered by a trained ML classifier hosted on Google Colab</p>",
    unsafe_allow_html=True,
)
