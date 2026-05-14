import streamlit as st
import requests
import re

st.set_page_config(page_title="CodeFix", page_icon="⚡", layout="wide")

st.markdown("""
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><defs><linearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'><stop offset='0%25' stop-color='%23818cf8'/><stop offset='100%25' stop-color='%23f472b6'/></linearGradient></defs><rect width='100' height='100' rx='22' fill='%23050510'/><text x='50' y='62' font-size='54' font-family='monospace' font-weight='900' text-anchor='middle' fill='url(%23g)'>&lt;/&gt;</text></svg>">
""", unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #050510;
    color: #e2e8f0;
}

.stApp {
    background: #050510;
    min-height: 100vh;
    overflow-x: hidden;
}

/* Hexagon background pattern */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(circle at 20% 20%, rgba(109,40,217,0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(59,130,246,0.1) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(139,92,246,0.05) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* Hero section */
.hero-section {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 4rem 2rem 3rem;
    position: relative;
    max-width: 1200px;
    margin: 0 auto;
}

.hero-left { flex: 1; max-width: 600px; }

.hero-tag {
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: rgba(139,92,246,0.1);
    border: 1px solid rgba(139,92,246,0.3);
    color: #a78bfa; font-size: 0.7rem; font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase;
    padding: 0.4rem 1rem; border-radius: 100px;
    margin-bottom: 1.5rem;
}

.hero-title {
    font-size: 4.5rem; font-weight: 900; line-height: 1;
    letter-spacing: -0.04em; margin-bottom: 1rem;
}
.hero-title .line1 { color: #f1f5f9; display: block; }
.hero-title .line2 {
    display: block; font-size: 2.8rem;
    background: linear-gradient(135deg, #818cf8 0%, #a78bfa 40%, #f472b6 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}

.hero-desc {
    font-size: 1.05rem; color: #64748b; line-height: 1.7;
    margin-bottom: 2rem; max-width: 440px;
}

.hero-pills {
    display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 2rem;
}
.h-pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #94a3b8; font-size: 0.75rem; font-weight: 500;
    padding: 0.35rem 0.9rem; border-radius: 100px;
}

.hero-stats {
    display: flex; gap: 2rem;
}
.stat { text-align: left; }
.stat-num {
    font-size: 1.5rem; font-weight: 800; color: #f1f5f9;
    background: linear-gradient(135deg, #818cf8, #f472b6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.stat-label { font-size: 0.7rem; color: #475569; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.2rem; }

/* 3D Geometric shape */
.hero-right {
    flex: 0 0 380px;
    display: flex; align-items: center; justify-content: center;
    position: relative; height: 380px;
}

.geo-wrap {
    position: relative; width: 300px; height: 300px;
    animation: float 6s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0px) rotateY(0deg); }
    33% { transform: translateY(-15px) rotateY(5deg); }
    66% { transform: translateY(-8px) rotateY(-3deg); }
}

.geo-glow {
    position: absolute; inset: -40px;
    background: radial-gradient(circle, rgba(139,92,246,0.3) 0%, transparent 70%);
    border-radius: 50%; filter: blur(20px);
    animation: glow-pulse 3s ease-in-out infinite;
}
@keyframes glow-pulse {
    0%, 100% { opacity: 0.6; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.1); }
}

.hex-grid {
    position: absolute; inset: 0; opacity: 0.15;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='100' viewBox='0 0 56 100'%3E%3Cpath d='M28 66L0 50V17L28 0l28 17v33L28 66zm0-2l26-15V19L28 2 2 19v30l26 15z' fill='%23818cf8'/%3E%3Cpath d='M28 100L0 83V67l28 16 28-16v16L28 100zm0-2l26-15V69l-26 15-26-15v12l26 15z' fill='%23818cf8'/%3E%3C/svg%3E");
}

/* Main content wrapper */
.main-wrap {
    max-width: 860px;
    margin: 0 auto;
    padding: 0 1.5rem 3rem;
    position: relative;
    z-index: 1;
}

/* Section divider */
.sec-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.3), transparent);
    margin: 2rem 0;
}

/* Card style for selectors */
.card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
}

/* Labels */
.sel-label {
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: #7c3aed; margin-bottom: 0.5rem;
}
.sec-label {
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: #7c3aed; margin: 1.5rem 0 0.5rem;
}
.level-hint {
    font-size: 0.7rem; color: #475569; margin-top: 0.4rem; line-height: 1.5;
}

/* Hide default widget labels only — NOT the radio option labels */
div[data-testid="stRadio"] [data-testid="stWidgetLabel"] { display: none !important; }
div[data-testid="stSelectbox"] [data-testid="stWidgetLabel"] { display: none !important; }
div[data-testid="stTextArea"] [data-testid="stWidgetLabel"] { display: none !important; }

/* Radio fix */
div[data-testid="stRadio"] > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important; padding: 0.6rem 1rem !important;
}
div[data-testid="stRadio"] label {
    color: #e2e8f0 !important; font-size: 0.9rem !important;
    display: flex !important; visibility: visible !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
}

/* Inputs */
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important; color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.875rem !important; line-height: 1.7 !important;
}
.stTextArea textarea:focus {
    border-color: rgba(124,58,237,0.6) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}
.stTextArea textarea::placeholder { color: #1e293b !important; }

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #4c1d95 0%, #6d28d9 50%, #7c3aed 100%) !important;
    color: #ffffff !important; border: 1px solid rgba(139,92,246,0.4) !important;
    border-radius: 12px !important; padding: 0.9rem 2rem !important;
    font-weight: 700 !important; font-size: 1rem !important;
    transition: all 0.3s ease !important; width: 100% !important;
    box-shadow: 0 0 30px rgba(109,40,217,0.3), inset 0 1px 0 rgba(255,255,255,0.1) !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 50px rgba(109,40,217,0.5), inset 0 1px 0 rgba(255,255,255,0.15) !important;
}

/* Response blocks */
.res-header {
    display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;
    padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.res-dot {
    width: 8px; height: 8px; background: #22c55e; border-radius: 50%;
    box-shadow: 0 0 10px #22c55e;
    animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.4} }
.res-title { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #22c55e; }

.block { border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 0.75rem; font-size: 0.93rem; line-height: 1.8; position: relative; overflow: hidden; }
.block::before { content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; border-radius: 3px 0 0 3px; }
.block-error { background: rgba(239,68,68,0.06); border: 1px solid rgba(239,68,68,0.15); }
.block-error::before { background: #ef4444; }
.block-why { background: rgba(234,179,8,0.06); border: 1px solid rgba(234,179,8,0.15); }
.block-why::before { background: #eab308; }
.block-improve { background: rgba(59,130,246,0.06); border: 1px solid rgba(59,130,246,0.15); }
.block-improve::before { background: #3b82f6; }
.block-remember { background: rgba(139,92,246,0.08); border: 1px solid rgba(139,92,246,0.25); font-weight: 500; }
.block-remember::before { background: #8b5cf6; }
.block-concept { background: rgba(234,179,8,0.06); border: 1px solid rgba(234,179,8,0.15); }
.block-concept::before { background: #eab308; }
.block-analogy { background: rgba(59,130,246,0.06); border: 1px solid rgba(59,130,246,0.15); }
.block-analogy::before { background: #3b82f6; }
.blk-title { font-size: 0.62rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 0.6rem; }
.blk-title.error { color: #f87171; }
.blk-title.why { color: #fbbf24; }
.blk-title.fixed { color: #4ade80; }
.blk-title.improve { color: #60a5fa; }
.blk-title.remember { color: #c084fc; }
.blk-title.concept { color: #fbbf24; }
.blk-title.analogy { color: #60a5fa; }

hr { border-color: rgba(255,255,255,0.04) !important; margin: 2rem 0 !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# --- API ---
GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_groq(prompt):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    body = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    response = requests.post(GROQ_URL, headers=headers, json=body)
    result = response.json()
    if "choices" not in result:
        raise Exception(f"API Error: {result}")
    return result["choices"][0]["message"]["content"]

def extract_section(text, heading):
    pattern = rf'\*\*{re.escape(heading)}\*\*\s*(.*?)(?=\*\*[A-Z]|\Z)'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

# --- Hero Section ---
st.markdown("""
<div class="hero-section">
    <div class="hero-left">
        <div class="hero-tag">⚡ CRISP Framework · AI-Powered · Free</div>
        <div class="hero-title">
            <div class="cf-logo">
                <svg width="52" height="52" viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg" style="display:block;margin-bottom:0.6rem">
                    <defs>
                        <linearGradient id="lg1" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#818cf8"/>
                            <stop offset="100%" stop-color="#f472b6"/>
                        </linearGradient>
                    </defs>
                    <rect width="52" height="52" rx="14" fill="rgba(129,140,248,0.1)" stroke="rgba(129,140,248,0.3)" stroke-width="1"/>
                    <text x="26" y="34" font-size="22" font-family="monospace" font-weight="900" text-anchor="middle" fill="url(#lg1)">&lt;/&gt;</text>
                </svg>
            </div>
            <span class="line1">CodeFix.</span>
            <span class="line2">Learn why.</span>
        </div>
        <div class="hero-desc">
            CodeFix is an AI-powered coding tutor for engineering students.
            Not just a fixer — it diagnoses, explains, and teaches so you never repeat the same mistake.
        </div>
        <div class="hero-pills">
            <span class="h-pill">🐍 Python</span>
            <span class="h-pill">⚙️ C</span>
            <span class="h-pill">➕ C++</span>
        </div>
        <div class="hero-stats">
            <div class="stat">
                <div class="stat-num">CRISP</div>
                <div class="stat-label">Framework</div>
            </div>
            <div class="stat">
                <div class="stat-num">3</div>
                <div class="stat-label">Languages</div>
            </div>
            <div class="stat">
                <div class="stat-num">2</div>
                <div class="stat-label">Skill Levels</div>
            </div>
        </div>
    </div>
    <div class="hero-right">
        <div class="hex-grid"></div>
        <div class="geo-wrap">
            <div class="geo-glow"></div>
            <svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;filter:drop-shadow(0 0 30px rgba(139,92,246,0.6))">
                <defs>
                    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#818cf8;stop-opacity:1"/>
                        <stop offset="50%" style="stop-color:#a78bfa;stop-opacity:1"/>
                        <stop offset="100%" style="stop-color:#f472b6;stop-opacity:0.8"/>
                    </linearGradient>
                    <linearGradient id="g2" x1="100%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" style="stop-color:#312e81;stop-opacity:0.9"/>
                        <stop offset="100%" style="stop-color:#4c1d95;stop-opacity:0.7"/>
                    </linearGradient>
                    <linearGradient id="g3" x1="0%" y1="100%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:#1e1b4b;stop-opacity:0.95"/>
                        <stop offset="100%" style="stop-color:#312e81;stop-opacity:0.8"/>
                    </linearGradient>
                    <filter id="glow">
                        <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                        <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
                    </filter>
                </defs>
                <!-- Main diamond shape -->
                <polygon points="150,20 270,120 230,260 70,260 30,120" fill="url(#g2)" stroke="url(#g1)" stroke-width="1.5" filter="url(#glow)"/>
                <!-- Inner facets -->
                <polygon points="150,20 270,120 150,150" fill="url(#g3)" stroke="url(#g1)" stroke-width="0.8" opacity="0.9"/>
                <polygon points="150,20 30,120 150,150" fill="url(#g2)" stroke="url(#g1)" stroke-width="0.8" opacity="0.7"/>
                <polygon points="270,120 230,260 150,150" fill="url(#g3)" stroke="url(#g1)" stroke-width="0.8" opacity="0.8"/>
                <polygon points="30,120 70,260 150,150" fill="url(#g2)" stroke="url(#g1)" stroke-width="0.8" opacity="0.6"/>
                <polygon points="230,260 70,260 150,150" fill="url(#g3)" stroke="url(#g1)" stroke-width="0.8" opacity="0.85"/>
                <!-- Highlight edge -->
                <line x1="150" y1="20" x2="270" y2="120" stroke="#c4b5fd" stroke-width="2" opacity="0.6"/>
                <line x1="150" y1="20" x2="30" y2="120" stroke="#818cf8" stroke-width="1" opacity="0.4"/>
                <!-- Center glow dot -->
                <circle cx="150" cy="148" r="4" fill="#f472b6" opacity="0.9" filter="url(#glow)"/>
                <!-- Floating particles -->
                <circle cx="60" cy="60" r="2" fill="#a78bfa" opacity="0.6">
                    <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite"/>
                </circle>
                <circle cx="240" cy="80" r="1.5" fill="#818cf8" opacity="0.5">
                    <animate attributeName="opacity" values="0.5;0.9;0.5" dur="3s" repeatCount="indefinite"/>
                </circle>
                <circle cx="200" cy="240" r="2" fill="#f472b6" opacity="0.4">
                    <animate attributeName="opacity" values="0.4;0.8;0.4" dur="2.5s" repeatCount="indefinite"/>
                </circle>
                <circle cx="80" cy="200" r="1.5" fill="#a78bfa" opacity="0.5">
                    <animate attributeName="opacity" values="0.5;1;0.5" dur="1.8s" repeatCount="indefinite"/>
                </circle>
            </svg>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Main Content ---
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)
st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)

# --- Selectors ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="sel-label">🌐 Language</div>', unsafe_allow_html=True)
    language = st.selectbox("Language", ["Python", "C", "C++"], label_visibility="collapsed")
with col2:
    st.markdown('<div class="sel-label">🔀 Mode</div>', unsafe_allow_html=True)
    mode = st.radio("Mode", ["Code Doubt", "Concept Doubt"], label_visibility="collapsed")
with col3:
    st.markdown('<div class="sel-label">📊 Level</div>', unsafe_allow_html=True)
    level = st.radio("Level", ["Beginner", "Intermediate"], label_visibility="collapsed")
    if level == "Beginner":
        st.markdown('<div class="level-hint">🟢 Simple language, analogies, no jargon</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="level-hint">🔵 Technical depth, best practices, edge cases</div>', unsafe_allow_html=True)

st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)

if mode == "Code Doubt":
    st.markdown('<div class="sec-label">📋 Paste Your Code</div>', unsafe_allow_html=True)
    user_code = st.text_area("Your Code", height=180, placeholder="# Paste your buggy code here...", label_visibility="collapsed")
    st.markdown('<div class="sec-label">⚠️ Error / Output You Got</div>', unsafe_allow_html=True)
    error_msg = st.text_area("Error Message", height=80, placeholder="Paste the error message or wrong output here...", label_visibility="collapsed")
    user_question = ""
else:
    user_code = ""
    error_msg = ""
    st.markdown('<div class="sec-label">💭 Your Concept Doubt</div>', unsafe_allow_html=True)
    user_question = st.text_area("Your Doubt", height=120, placeholder="e.g. What is recursion? How do pointers work in C?", label_visibility="collapsed")

st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
submit = st.button("🔍   Solve My Doubt", use_container_width=True)

if submit:
    if mode == "Code Doubt" and not user_code.strip():
        st.warning("Please paste your code before submitting.")
    elif mode == "Concept Doubt" and not user_question.strip():
        st.warning("Please type your concept doubt before submitting.")
    else:
        with st.spinner("CodeFix is analyzing..."):
            if mode == "Code Doubt":
                prompt = f"""
**Context:** You are CodeFix, an AI coding tutor for {level} level engineering students learning {language}.
**Role:** For Beginner: simple language, analogies, no jargon. For Intermediate: technical depth, best practices.
**Instructions:** Analyze code and error. Teach — don't just fix.
**Parameters:** Use EXACTLY these headings:

**Error Diagnosis**
[exact mistake and line number]

**Why This Happened**
[root cause for {level} student]

**Fixed Code**
[corrected code only]

**Code Improvement**
[one improvement suggestion]

**Remember This**
[one short memorable rule]

Code: {user_code}
Error: {error_msg if error_msg.strip() else "No error message provided."}
"""
            else:
                prompt = f"""
**Context:** You are CodeFix, an AI coding tutor for {level} level engineering students studying {language}.
**Role:** For Beginner: simple, analogies, no jargon. For Intermediate: technical depth, edge cases, best practices.
**Parameters:** Use EXACTLY these headings:

**Concept Explanation**
[explain for {level} level]

**Example**
[short {language} code only]

**Real-World Analogy**
[relatable analogy]

**Remember This**
[one memorable takeaway]

Doubt: {user_question}
"""
            try:
                answer = ask_groq(prompt)
                st.markdown('<div class="res-header"><div class="res-dot"></div><div class="res-title">CodeFix Response</div></div>', unsafe_allow_html=True)

                if mode == "Code Doubt":
                    diagnosis = extract_section(answer, "Error Diagnosis")
                    why = extract_section(answer, "Why This Happened")
                    fixed = extract_section(answer, "Fixed Code")
                    improvement = extract_section(answer, "Code Improvement")
                    remember = extract_section(answer, "Remember This")

                    if diagnosis:
                        st.markdown(f'<div class="block block-error"><div class="blk-title error">🔴 Error Diagnosis</div>{diagnosis}</div>', unsafe_allow_html=True)
                    if why:
                        st.markdown(f'<div class="block block-why"><div class="blk-title why">🟡 Why This Happened</div>{why}</div>', unsafe_allow_html=True)
                    if fixed:
                        st.markdown('<div class="blk-title fixed" style="margin:0.75rem 0 0.4rem;font-size:0.62rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;">🟢 Fixed Code</div>', unsafe_allow_html=True)
                        st.code(fixed.replace("```python","").replace("```c","").replace("```","").strip(), language="python" if language=="Python" else "c")
                    if improvement:
                        st.markdown(f'<div class="block block-improve"><div class="blk-title improve">🔵 Code Improvement</div>{improvement}</div>', unsafe_allow_html=True)
                    if remember:
                        st.markdown(f'<div class="block block-remember"><div class="blk-title remember">💜 Remember This</div>{remember}</div>', unsafe_allow_html=True)
                else:
                    explanation = extract_section(answer, "Concept Explanation")
                    example = extract_section(answer, "Example")
                    analogy = extract_section(answer, "Real-World Analogy")
                    remember = extract_section(answer, "Remember This")

                    if explanation:
                        st.markdown(f'<div class="block block-concept"><div class="blk-title concept">💡 Concept Explanation</div>{explanation}</div>', unsafe_allow_html=True)
                    if example:
                        st.markdown('<div class="blk-title fixed" style="margin:0.75rem 0 0.4rem;font-size:0.62rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;">🟢 Example</div>', unsafe_allow_html=True)
                        st.code(example.replace("```python","").replace("```c","").replace("```","").strip(), language="python" if language=="Python" else "c")
                    if analogy:
                        st.markdown(f'<div class="block block-analogy"><div class="blk-title analogy">🔵 Real-World Analogy</div>{analogy}</div>', unsafe_allow_html=True)
                    if remember:
                        st.markdown(f'<div class="block block-remember"><div class="blk-title remember">💜 Remember This</div>{remember}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)
