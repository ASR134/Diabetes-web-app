import streamlit as st
import requests
import json
import time

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GlucoSense · Diabetes Risk Analyzer",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root variables ── */
:root {
    --bg:       #0b0f1a;
    --surface:  #131929;
    --border:   #1e2d4a;
    --teal:     #00d4b1;
    --teal-dim: #00a88e;
    --amber:    #f5a623;
    --red:      #ff5f6d;
    --text:     #e8edf7;
    --muted:    #7a8baa;
    --card-bg:  #0e1625;
}

/* ── Base reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

.stApp {
    background: radial-gradient(ellipse at 20% 0%, #0d2240 0%, #0b0f1a 55%),
                radial-gradient(ellipse at 80% 100%, #041a2e 0%, transparent 60%);
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header, .stDeployButton { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(0,212,177,0.15), rgba(0,212,177,0.05));
    border: 1px solid rgba(0,212,177,0.3);
    color: var(--teal);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 20px;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    font-weight: 400;
    line-height: 1.1;
    margin: 0 0 0.8rem;
    background: linear-gradient(135deg, #e8edf7 30%, #00d4b1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero h1 em {
    font-style: italic;
    background: linear-gradient(135deg, #00d4b1, #00a88e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── Section labels ── */
.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--teal);
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
}

/* ── Input cards ── */
[data-testid="column"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 1.4rem 1.2rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="column"]:hover {
    border-color: rgba(0,212,177,0.25) !important;
}

/* ── Streamlit number inputs ── */
[data-testid="stNumberInput"] label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    letter-spacing: 0.02em !important;
    margin-bottom: 0.3rem !important;
}
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-size: 1.05rem !important;
    font-weight: 500 !important;
    transition: border-color 0.2s !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(0,212,177,0.1) !important;
}
[data-testid="stNumberInput"] button {
    background: var(--border) !important;
    border: none !important;
    color: var(--text) !important;
}
[data-testid="stNumberInput"] button:hover {
    background: var(--teal-dim) !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 2rem 0 !important;
}

/* ── Predict button ── */
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #00d4b1, #0099ff) !important;
    color: #0b0f1a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 1.5rem !important;
    height: 3.2rem !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    box-shadow: 0 4px 20px rgba(0,212,177,0.35) !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(0,212,177,0.5) !important;
}
[data-testid="stButton"] > button[kind="primary"]:active {
    transform: translateY(0) !important;
}

/* ── Result cards ── */
.result-safe {
    background: linear-gradient(135deg, rgba(0,212,177,0.08), rgba(0,212,177,0.03));
    border: 1px solid rgba(0,212,177,0.4);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
}
.result-safe .result-icon { font-size: 3rem; margin-bottom: 0.5rem; }
.result-safe .result-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    color: var(--teal);
    margin-bottom: 0.4rem;
}
.result-safe .result-sub { color: var(--muted); font-size: 0.9rem; }

.result-risk {
    background: linear-gradient(135deg, rgba(255,95,109,0.08), rgba(245,166,35,0.04));
    border: 1px solid rgba(255,95,109,0.4);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
}
.result-risk .result-icon { font-size: 3rem; margin-bottom: 0.5rem; }
.result-risk .result-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    color: var(--red);
    margin-bottom: 0.4rem;
}
.result-risk .result-sub { color: var(--muted); font-size: 0.9rem; }

/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}
.stat-card {
    flex: 1;
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.stat-card .stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: var(--teal);
    display: block;
}
.stat-card .stat-lbl {
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    color: var(--muted) !important;
    font-size: 0.85rem !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--teal) !important; }

/* ── Alert / toast overrides ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
}

/* ── Footer ── */
.app-footer {
    text-align: center;
    padding: 2rem 0 3rem;
    color: var(--muted);
    font-size: 0.78rem;
    line-height: 1.8;
    border-top: 1px solid var(--border);
    margin-top: 2rem;
}
.app-footer strong { color: var(--text); }

/* ── Tooltip help text ── */
.stTooltipIcon { color: var(--muted) !important; }

/* ── Progress bar for risk indicator ── */
.risk-meter {
    background: var(--border);
    border-radius: 10px;
    height: 8px;
    margin: 1rem 0 0.4rem;
    overflow: hidden;
    position: relative;
}
.risk-fill-low {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, var(--teal), #00ff9d);
    width: 15%;
    animation: fill-in 1s ease forwards;
}
.risk-fill-high {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, var(--amber), var(--red));
    width: 80%;
    animation: fill-in 1s ease forwards;
}
@keyframes fill-in {
    from { transform: scaleX(0); transform-origin: left; }
    to   { transform: scaleX(1); transform-origin: left; }
}

/* Columns gap */
[data-testid="stHorizontalBlock"] {
    gap: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── API ───────────────────────────────────────────────────────────────────────
API_URL = "https://diabetes-prediction-api-ekdt.onrender.com/predict"

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">🩺 AI-Powered Health Assessment</div>
  <h1>Know Your Risk.<br><em>Act Early.</em></h1>
  <p>Enter your clinical parameters below and let our model assess your diabetes risk in seconds.</p>
</div>
""", unsafe_allow_html=True)

# ── Quick stats row ───────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
  <div class="stat-card">
    <span class="stat-num">8</span>
    <div class="stat-lbl">Biomarkers</div>
  </div>
  <div class="stat-card">
    <span class="stat-num">~1s</span>
    <div class="stat-lbl">Analysis Time</div>
  </div>
  <div class="stat-card">
    <span class="stat-num">ML</span>
    <div class="stat-lbl">Powered</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Section: Clinical Inputs ──────────────────────────────────────────────────
st.markdown('<div class="section-label">Clinical Parameters</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    pregnancies = st.number_input(
        "Pregnancies", min_value=0, max_value=20, value=0, step=1,
        help="Number of times pregnant"
    )
    glucose = st.number_input(
        "Glucose (mg/dL)", min_value=1, max_value=300, value=100, step=1,
        help="Plasma glucose concentration (2-hour oral glucose tolerance test)"
    )
    blood_pressure = st.number_input(
        "Blood Pressure (mm Hg)", min_value=1, max_value=200, value=70, step=1,
        help="Diastolic blood pressure"
    )
    skin_thickness = st.number_input(
        "Skin Thickness (mm)", min_value=0, max_value=100, value=20, step=1,
        help="Triceps skin fold thickness"
    )

with col2:
    insulin = st.number_input(
        "Insulin (mu U/ml)", min_value=0, max_value=900, value=80, step=1,
        help="2-Hour serum insulin"
    )
    bmi = st.number_input(
        "BMI", min_value=0.1, max_value=49.9, value=25.0, step=0.1,
        help="Body mass index — weight (kg) / height² (m)"
    )
    diabetes_pedigree = st.number_input(
        "Pedigree Function", min_value=0.0, max_value=2.5, value=0.5, step=0.01,
        help="Diabetes pedigree function (family history score)"
    )
    age = st.number_input(
        "Age (years)", min_value=1, max_value=119, value=25, step=1,
        help="Age in years"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Predict button ────────────────────────────────────────────────────────────
predict_clicked = st.button("⚡  Analyze Risk Now", type="primary", use_container_width=True)

# ── Prediction logic ──────────────────────────────────────────────────────────
if predict_clicked:
    data = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": diabetes_pedigree,
        "Age": age,
    }

    try:
        with st.spinner("Running analysis…"):
            time.sleep(0.4)
            response = requests.post(API_URL, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            prediction_result = result.get("predicted category ", "Unknown")

            st.markdown('<div class="section-label">Prediction Result</div>', unsafe_allow_html=True)

            if prediction_result == "Non Diabetic":
                st.markdown("""
                <div class="result-safe">
                  <div class="result-icon">✅</div>
                  <div class="result-title">Non-Diabetic</div>
                  <div class="result-sub">Your parameters suggest a lower diabetes risk. Keep maintaining a healthy lifestyle.</div>
                  <div class="risk-meter"><div class="risk-fill-low"></div></div>
                  <small style="color:#7a8baa;font-size:0.72rem;">Low risk indicator</small>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown("""
                <div class="result-risk">
                  <div class="result-icon">⚠️</div>
                  <div class="result-title">Diabetic Risk Detected</div>
                  <div class="result-sub">Your parameters suggest an elevated risk. Please consult a healthcare professional promptly.</div>
                  <div class="risk-meter"><div class="risk-fill-high"></div></div>
                  <small style="color:#7a8baa;font-size:0.72rem;">High risk indicator</small>
                </div>
                """, unsafe_allow_html=True)

            # Input summary
            with st.expander("📋 View full parameter summary"):
                st.json(data)

        else:
            st.error(f"API returned status {response.status_code}. Details: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not reach the prediction API. Please check your connection or server status.")
    except requests.exceptions.Timeout:
        st.error("⏱ The request timed out. The API server may be waking up — please try again in a moment.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
  <strong>GlucoSense</strong> · AI Diabetes Risk Analyzer<br>
  <span>This tool is for informational purposes only and does not constitute medical advice.<br>
  Always consult a qualified healthcare professional for diagnosis and treatment.</span>
</div>
""", unsafe_allow_html=True)