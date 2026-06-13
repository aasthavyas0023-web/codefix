import streamlit as st
import requests
import subprocess
import tempfile
import os
import sys
import time
import json
from datetime import datetime

st.set_page_config(page_title="CodeFix", page_icon="🎯", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #080c14;
    color: #e2e8f0;
}
.stApp { background-color: #080c14; }

/* ── hide streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stDecoration"] { display: none; }

/* ── tab nav ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 0;
    border-bottom: 1px solid #1e293b;
    padding: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1.2rem !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #e2e8f0 !important;
    border-bottom: 2px solid #7c3aed !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 0 !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ── brand bar ── */
.brand-bar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 0 0.5rem;
    border-bottom: 1px solid #1e293b;
    margin-bottom: 0;
}
.brand-dot {
    width: 8px; height: 8px;
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    border-radius: 50%;
}
.brand-name {
    font-size: 0.95rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: 0.03em;
}

/* ── hero ── */
.hero-section { padding: 3.5rem 0 2rem; }
.hero-title {
    font-size: 3.4rem;
    font-weight: 700;
    line-height: 1.1;
    color: #f1f5f9;
    margin: 0 0 0.1rem;
}
.hero-sub {
    font-size: 2rem;
    font-weight: 600;
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 1rem;
}
.hero-desc {
    color: #94a3b8;
    font-size: 0.95rem;
    max-width: 520px;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}
.lang-badges { display: flex; gap: 0.5rem; margin-bottom: 2rem; }
.lang-badge {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 6px;
    padding: 0.25rem 0.7rem;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    color: #7c3aed;
    font-weight: 500;
}
.stat-cards { display: flex; gap: 0.75rem; margin-bottom: 2rem; }
.stat-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    min-width: 140px;
}
.stat-card .sc-title {
    font-size: 0.78rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 0.15rem;
}
.stat-card .sc-sub {
    font-size: 0.68rem;
    color: #64748b;
    font-weight: 400;
}
.hero-btns { display: flex; gap: 0.75rem; }
.btn-primary {
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.65rem 1.4rem;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.88rem;
    cursor: pointer;
}
.btn-ghost {
    background: transparent;
    color: #e2e8f0;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 0.65rem 1.4rem;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 500;
    font-size: 0.88rem;
    cursor: pointer;
}
.section-heading {
    font-size: 1.1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin: 2.5rem 0 1rem;
}
.feature-cards { display: flex; gap: 0.75rem; }
.feature-card {
    flex: 1;
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.2rem;
}
.feature-card .fc-icon {
    font-size: 1.2rem;
    margin-bottom: 0.6rem;
}
.feature-card .fc-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 0.3rem;
}
.feature-card .fc-desc {
    font-size: 0.75rem;
    color: #64748b;
    line-height: 1.5;
}

/* ── solve page layout ── */
.config-panel {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.2rem;
    height: 100%;
}
.cp-title {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #7c3aed;
    margin-bottom: 0.2rem;
}
.cp-label-small {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin: 1rem 0 0.4rem;
}
.ai-context-box {
    background: rgba(124,58,237,0.08);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 8px;
    padding: 0.7rem 0.8rem;
    margin-top: 1rem;
    font-size: 0.73rem;
    color: #a78bfa;
    line-height: 1.5;
}
.ai-context-box strong { color: #c4b5fd; display: block; margin-bottom: 0.2rem; }

/* ── editor panel ── */
.editor-panel {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    overflow: hidden;
}
.editor-topbar {
    background: #0a0f1e;
    border-bottom: 1px solid #1e293b;
    padding: 0.5rem 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.dot-red   { width:10px;height:10px;border-radius:50%;background:#f87171; }
.dot-yellow{ width:10px;height:10px;border-radius:50%;background:#fbbf24; }
.dot-green { width:10px;height:10px;border-radius:50%;background:#34d399; }
.file-tab {
    background: #1e293b;
    border-radius: 4px;
    padding: 0.15rem 0.6rem;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    color: #94a3b8;
    margin-left: 0.3rem;
}
.editor-body { padding: 0 0.4rem; }

.editor-footer {
    background: #0a0f1e;
    border-top: 1px solid #1e293b;
    padding: 0.6rem 0.8rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.7rem;
    color: #475569;
}
.footer-badges { display: flex; gap: 0.6rem; }
.f-badge { display: flex; align-items: center; gap: 0.3rem; }

/* ── streamlit widget overrides inside editor ── */
.stTextArea textarea {
    background-color: #080c14 !important;
    border: none !important;
    border-radius: 0 !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.83rem !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    box-shadow: none !important;
    border: none !important;
}
.stTextArea [data-baseweb="textarea"] { border: none !important; background: transparent !important; }
.stSelectbox > div > div {
    background-color: #080c14 !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-size: 0.85rem !important;
}
.stRadio > div { background: transparent; border: none; padding: 0; gap: 0.4rem !important; }
.stRadio label {
    background: #080c14 !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    padding: 0.45rem 0.9rem !important;
    color: #64748b !important;
    font-size: 0.82rem !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
}
.stRadio label:has(input:checked) {
    background: rgba(124,58,237,0.15) !important;
    border-color: #7c3aed !important;
    color: #c4b5fd !important;
}

/* ── solve button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #7c3aed, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.4rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    transition: opacity 0.2s !important;
}
div[data-testid="stButton"] > button:hover { opacity: 0.85 !important; }

/* ── response breakdown ── */
.breakdown-header {
    padding: 1.5rem 0 0.5rem;
    border-bottom: 1px solid #1e293b;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
}
.bh-badge {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.3);
    color: #a78bfa;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    margin-bottom: 0.5rem;
    display: inline-block;
}
.bh-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #f1f5f9;
}
.resp-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.2rem 1.3rem;
    height: 100%;
    margin-bottom: 0.8rem;
}
.resp-card .rc-head {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.8rem;
}
.resp-card .rc-icon { font-size: 1rem; }
.resp-card .rc-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: #e2e8f0;
}
.resp-card.card-error   { border-left: 3px solid #f87171; }
.resp-card.card-why     { border-left: 3px solid #fbbf24; }
.resp-card.card-fix     { border-left: 3px solid #34d399; }
.resp-card.card-improve { border-left: 3px solid #3b82f6; }
.resp-card.card-remember{ border-left: 3px solid #7c3aed; }
.resp-card .rc-body     { font-size: 0.82rem; color: #94a3b8; line-height: 1.65; }
.resp-card.card-error .rc-body.rc-concept  { font-size: 1rem; line-height: 1.75; }
.resp-card.card-why .rc-body.rc-analogy    { font-size: 1rem; line-height: 1.75; }

hr { border-color: #1e293b !important; margin: 1rem 0 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Persistent History — saved to JSON so it survives page refresh
# ─────────────────────────────────────────────────────────────────────────────
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "codefix_history.json")

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []

def save_history(history):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

if "history" not in st.session_state:
    st.session_state.history = load_history()
if "breakdown" not in st.session_state:
    st.session_state.breakdown = None


# ─────────────────────────────────────────────────────────────────────────────
#  API — Grok (xAI) with retry on rate limit
# ─────────────────────────────────────────────────────────────────────────────
GROK_API_KEY = st.secrets["GROK_API_KEY"]
GROK_URL     = "https://api.groq.com/openai/v1/chat/completions"

def ask_gemini(prompt: str, retries: int = 3) -> str:
    """Calls Grok API. Function name kept as ask_gemini so nothing else needs changing."""
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {GROK_API_KEY}",
    }
    body = {
        "model":    "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048,
    }
    last_err = ""
    for attempt in range(retries):
        try:
            resp   = requests.post(GROK_URL, headers=headers, json=body, timeout=60)
            result = resp.json()
            if resp.status_code == 200:
                return result["choices"][0]["message"]["content"]
            if resp.status_code in (429, 503):
                wait = 20 * (attempt + 1)
                st.toast(f"⏳ Groq rate limit — retrying in {wait}s…", icon="⚠️")
                time.sleep(wait)
                last_err = f"HTTP {resp.status_code} — rate limit"
                continue
            raise Exception(str(result))
        except requests.exceptions.Timeout:
            last_err = "Request timed out"
            time.sleep(5)
    raise Exception(f"Groq API failed after {retries} attempts: {last_err}")


# ─────────────────────────────────────────────────────────────────────────────
#  Code runner
# ─────────────────────────────────────────────────────────────────────────────
def run_code(code: str, language: str, mock_input: str = None):
    py = "python" if sys.platform == "win32" else "python3"
    stdin_data = (mock_input.strip() + "\n") if mock_input and mock_input.strip() else None
    try:
        if language == "Python":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
                f.write(code); src = f.name
            try:
                r = subprocess.run([py, src], input=stdin_data, capture_output=True, text=True, timeout=10)
                return r.stdout, r.stderr
            except subprocess.TimeoutExpired:
                return "", "TimeoutError: execution exceeded 10 seconds."
            except FileNotFoundError:
                return "", "Python interpreter not found."
            finally:
                try: os.unlink(src)
                except: pass

        ext = ".c" if language == "C" else ".cpp"
        cc  = "gcc" if language == "C" else "g++"
        with tempfile.NamedTemporaryFile(mode="w", suffix=ext, delete=False, encoding="utf-8") as f:
            f.write(code); src = f.name
        exe = src.replace(ext, ".out")
        try:
            cp = subprocess.run([cc, src, "-o", exe], capture_output=True, text=True, timeout=15)
            if cp.returncode != 0:
                return "", cp.stderr
            r = subprocess.run([exe], input=stdin_data, capture_output=True, text=True, timeout=10)
            return r.stdout, r.stderr
        except subprocess.TimeoutExpired:
            return "", "TimeoutError: execution exceeded 10 seconds."
        except FileNotFoundError:
            return "", f"{cc} not found. Install MinGW (Windows) or build-essential (Linux)."
        finally:
            for p in (src, exe):
                try: os.unlink(p)
                except: pass
    except Exception as e:
        return "", f"Runner error: {e}"


# ─────────────────────────────────────────────────────────────────────────────
#  Prompt builders
# ─────────────────────────────────────────────────────────────────────────────
def build_code_prompt(language, level, code, stdout, stderr):
    if level == "Beginner":
        level_instructions = """
STRICT BEGINNER RULES — follow every one:
- Error Diagnosis: state the error in ONE simple sentence. No jargon. Use ONLY the exact line number shown in the Runtime Error traceback. Never guess or adjust line numbers. Explain what went wrong in plain English.
- Why This Happened: explain like you are talking to someone who just started coding this week. Use a real-life analogy (e.g. "It's like calling a friend by the wrong name — Python can't find what you're asking for."). Maximum 3 sentences. Zero technical terms.
- Fixed Code: provide the corrected code with a short comment on the fixed line explaining what changed.
- Code Improvement: give ONE very basic tip a total beginner can apply immediately (e.g. "Always double-check spelling of function names before running.").
- Remember This: one short friendly sentence with no jargon (e.g. "Python reads exactly what you type — even one wrong letter causes an error.").
"""
    else:
        level_instructions = """
STRICT INTERMEDIATE RULES — follow every one:
- Error Diagnosis: state the error type, use ONLY the exact line number shown in the Runtime Error traceback, and explain the specific cause using correct technical terminology. Never infer or modify the reported line number.
- Why This Happened: explain the underlying mechanism — how Python's name resolution / memory model / type system causes this error. Reference relevant concepts (scope, stack, type coercion, pointer arithmetic, etc.). Minimum 3 technical sentences.
- Fixed Code: provide the corrected code. Add an inline comment explaining WHY the fix works at a technical level.
- Code Improvement: suggest a meaningful best practice — e.g. use of linters, exception handling patterns, memory management, time complexity improvement, or PEP8/style standards.
- Remember This: a concise technical rule the student can recall in an exam or interview (e.g. "Python resolves names using LEGB scope — Local → Enclosing → Global → Built-in.").
"""

return f"""
You are CodeFix, an AI coding tutor for 1st/2nd year engineering students learning {language}.
The student selected level: {level}.
The student's code was executed automatically. Real output and errors are captured below.

{level_instructions}

VERY IMPORTANT: Even if there are NO runtime errors and NO compiler errors, you MUST still:
- Carefully read every line of the code
- Check for logic errors (wrong loop bounds, wrong starting index, off-by-one mistakes)
- Check for semantic errors (code runs but gives wrong or unexpected output)
- Check for undefined behavior (division by zero, array out of bounds in C/C++)
- Check for bad coding habits or inefficient patterns
Do NOT just say "code ran successfully" — always diagnose deeply even for clean-running code.

Respond using EXACTLY these bold headings in this order and nothing else:

**Error Diagnosis**

**Why This Happened**

**Fixed Code**

**Code Improvement**

**Remember This**

---
{language} Code:
{code}

Execution Output:
{stdout.strip() if stdout.strip() else "(no output)"}

Runtime Error:
{stderr.strip() if stderr.strip() else "(none — but check the code carefully for logic errors, wrong output, or undefined behavior)"}
"""

def build_concept_prompt(language, level, question):
    if level == "Beginner":
        level_instructions = """
STRICT BEGINNER RULES — follow every one:
- Concept Explanation: explain in the simplest possible words as if the student has never heard this term before. No technical jargon. Use short sentences. Maximum 4 sentences.
- Example: write the shortest possible working {language} code that shows the concept. Add a comment on every line explaining what it does in plain English.
- Real-World Analogy: give a fun, relatable analogy from daily life (food, school, mobile phones, etc.) that makes the concept click instantly.
- Remember This: one simple sentence with zero technical words that a beginner can repeat to themselves.
""".format(language=language)
    else:
        level_instructions = """
STRICT INTERMEDIATE RULES — follow every one:
- Concept Explanation: give a precise technical definition. Explain the internal mechanism — how it works under the hood (memory, call stack, compiler behaviour, etc.). Use correct CS terminology. Minimum 4 sentences.
- Example: write a non-trivial {language} code example that demonstrates an advanced or edge-case use of the concept. Add inline comments explaining the technical behaviour at each step.
- Real-World Analogy: use a technical or engineering analogy (e.g. CPU pipelines, database transactions, network packets) that connects to the CS concept at a deeper level.
- Remember This: a precise technical rule or formula the student can use in an exam or technical interview.
""".format(language=language)

    return f"""
You are CodeFix, an AI coding tutor for 1st/2nd year engineering students studying {language}.
The student selected level: {level}.

{level_instructions}

Respond using EXACTLY these bold headings in this order and nothing else:

**Concept Explanation**

**Example**

**Real-World Analogy**

**Remember This**

---
Student's Doubt:
{question}
"""

def parse_sections(text: str) -> dict:
    """Extract each **Heading** section from Groq response, stripping code fences."""
    import re
    sections = {}
    pattern = r"\*\*(.+?)\*\*\s*\n(.*?)(?=\n\*\*|\Z)"
    for m in re.finditer(pattern, text, re.DOTALL):
        val = m.group(2).strip()
        # Strip markdown code fences e.g. ```python ... ``` or ``` ... ```
        val = re.sub(r"^```[\w]*\n?", "", val)
        val = re.sub(r"\n?```$", "", val)
        val = val.strip()
        sections[m.group(1).strip()] = val
    return sections


# ─────────────────────────────────────────────────────────────────────────────
#  Brand bar
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand-bar">
    <div class="brand-dot"></div>
    <span class="brand-name">CodeFix</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  Tabs: Home | Solve | History
# ─────────────────────────────────────────────────────────────────────────────
tab_home, tab_solve, tab_history = st.tabs(["Home", "Solve", "History"])


# ════════════════════════════════════════════════════════════════════════════
#  HOME TAB
# ════════════════════════════════════════════════════════════════════════════
with tab_home:
    left, right = st.columns([1.1, 0.9])

    with left:
        st.markdown("""
        <div class="hero-section">
            <div class="hero-title">CodeFix.</div>
            <div class="hero-sub">Learn why.</div>
            <div class="hero-desc">
                Master the foundational architecture of high-performance code.
                CodeFix doesn't just show you what works — it reveals the
                <em>mechanics</em> of why, transforming syntax into deep technical intuition.
            </div>
            <div class="lang-badges">
                <span class="lang-badge">Python</span>
                <span class="lang-badge">C</span>
                <span class="lang-badge">C++</span>
            </div>
            <div class="stat-cards">
                <div class="stat-card">
                    <div class="sc-title">CRISP</div>
                    <div class="sc-sub">Clarity Engine</div>
                </div>
                <div class="stat-card">
                    <div class="sc-title">3 Languages</div>
                    <div class="sc-sub">Native Support</div>
                </div>
                <div class="stat-card">
                    <div class="sc-title">2 Skill Levels</div>
                    <div class="sc-sub">Adaptive Paths</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div style="padding:3rem 0 0; display:flex; justify-content:center;">
            <svg width="280" height="280" viewBox="0 0 280 280" fill="none" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <radialGradient id="g1" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.9"/>
                  <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.3"/>
                </radialGradient>
                <radialGradient id="g2" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stop-color="#c4b5fd" stop-opacity="0.6"/>
                  <stop offset="100%" stop-color="#7c3aed" stop-opacity="0.1"/>
                </radialGradient>
              </defs>
              <!-- outer ring -->
              <ellipse cx="140" cy="140" rx="110" ry="40" stroke="#7c3aed" stroke-width="1.5" stroke-opacity="0.4" fill="none" transform="rotate(-30 140 140)"/>
              <ellipse cx="140" cy="140" rx="110" ry="40" stroke="#3b82f6" stroke-width="1.5" stroke-opacity="0.3" fill="none" transform="rotate(30 140 140)"/>
              <!-- inner sphere -->
              <circle cx="140" cy="140" r="60" fill="url(#g1)" opacity="0.85"/>
              <circle cx="140" cy="140" r="60" fill="url(#g2)" opacity="0.4"/>
              <!-- highlight -->
              <circle cx="120" cy="118" r="18" fill="white" fill-opacity="0.08"/>
              <!-- orbiting dot -->
              <circle cx="210" cy="120" r="7" fill="#c4b5fd" opacity="0.9"/>
              <circle cx="75"  cy="165" r="5" fill="#3b82f6" opacity="0.7"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Engineered for the Flow State</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-cards">
        <div class="feature-card">
            <div class="fc-icon">🔴</div>
            <div class="fc-title">Live Execution</div>
            <div class="fc-desc">Your code runs inside CodeFix. Real errors, real output — no copy-paste needed.</div>
        </div>
        <div class="feature-card">
            <div class="fc-icon">⚡</div>
            <div class="fc-title">Deep Diagnosis</div>
            <div class="fc-desc">Not just "what's wrong" — CodeFix tells you why it broke and how to never repeat it.</div>
        </div>
        <div class="feature-card">
            <div class="fc-icon">📚</div>
            <div class="fc-title">Doubt History</div>
            <div class="fc-desc">Every doubt saved. Review code doubts and concept explanations any time from the sidebar.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  SOLVE TAB
# ════════════════════════════════════════════════════════════════════════════
with tab_solve:
    # ── INPUT PANEL — always visible ─────────────────────────────────────────
    cfg_col, editor_col = st.columns([0.38, 0.62])

    with cfg_col:
        st.markdown("""
        <div class="config-panel">
            <div class="cp-title">⚙ Configuration</div>
            <div style="font-size:0.7rem;color:#475569;margin-top:0.1rem;">CUSTOMIZE YOUR SESSION</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="cp-label-small">Programming Language</div>', unsafe_allow_html=True)
        language = st.selectbox("lang", ["Python", "C", "C++"], label_visibility="collapsed")

        st.markdown('<div class="cp-label-small">Query Mode</div>', unsafe_allow_html=True)
        mode = st.radio("mode", ["Code Doubt", "Concept Doubt"],
                        label_visibility="collapsed")

        st.markdown('<div class="cp-label-small">Experience Level</div>', unsafe_allow_html=True)
        level = st.radio("level", ["Beginner", "Intermediate"],
                         label_visibility="collapsed")

        mode_short = "Code" if mode == "Code Doubt" else "Concept"
        st.markdown(f"""
        <div class="ai-context-box">
            <strong>ℹ AI Context Active</strong>
            CodeFix is analyzing your {mode_short.lower()} structure using the {level} {language} profile.
        </div>
        """, unsafe_allow_html=True)

    with editor_col:
        ext_map = {"Python": "main.py", "C": "main.c", "C++": "main.cpp"}
        fname   = ext_map[language]

        if mode == "Code Doubt":
            st.markdown(f"""
            <div class="editor-topbar">
                <div class="dot-red"></div>
                <div class="dot-yellow"></div>
                <div class="dot-green"></div>
                <span class="file-tab">📄 {fname}</span>
                <span style="margin-left:auto;font-size:0.68rem;font-family:'JetBrains Mono',monospace;color:#475569;">{language}</span>
            </div>
            """, unsafe_allow_html=True)

            user_code = st.text_area(
                "code_in",
                height=220,
                placeholder="# Paste your code here — CodeFix will run it automatically",
                label_visibility="collapsed",
            )
            user_question = ""

            # ── Show sample input box if code uses input()/scanf/cin ──────────
            import re as _re
            _has_input = bool(
                (language == "Python" and _re.search(r'input\s*\(', user_code)) or
                (language == "C"      and _re.search(r'scanf\s*\(', user_code)) or
                (language == "C++"    and _re.search(r'cin\s*>>',   user_code))
            )
            if _has_input:
                st.markdown("""
                <div style="background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.3);
                border-radius:8px;padding:0.6rem 0.8rem;margin-top:0.5rem;font-size:0.75rem;color:#a78bfa;">
                    💡 <strong style="color:#c4b5fd;">Input detected</strong> — enter sample value(s) below
                    so CodeFix can run your code (one value per line)
                </div>
                """, unsafe_allow_html=True)
                mock_input_str = st.text_area(
                    "sample_input",
                    placeholder="e.g.  5",
                    height=80,
                    label_visibility="collapsed",
                    key="mock_input_box"
                )
            else:
                mock_input_str = ""

        else:
            st.markdown("""
            <div class="editor-topbar">
                <div class="dot-red"></div>
                <div class="dot-yellow"></div>
                <div class="dot-green"></div>
                <span class="file-tab">💡 concept_doubt</span>
            </div>
            """, unsafe_allow_html=True)

            user_question = st.text_area(
                "concept_in",
                height=220,
                placeholder="e.g. What is recursion? How do pointers work in C?",
                label_visibility="collapsed",
            )
            user_code = ""

        btn_label = "▶ Run & Debug" if mode == "Code Doubt" else "🔍 Explain This"
        fc1, fc2 = st.columns([1, 0.4])
        with fc1:
            st.markdown("""
            <div style="display:flex;gap:0.8rem;align-items:center;padding-top:0.5rem;">
                <span style="font-size:0.7rem;color:#475569;">⚡ AI Enhanced</span>
                <span style="font-size:0.7rem;color:#475569;">🔒 Privacy First</span>
            </div>
            """, unsafe_allow_html=True)
        with fc2:
            solve_btn = st.button(btn_label, use_container_width=True)

    # ── Submit logic ──────────────────────────────────────────────────────────
    if solve_btn:
        if mode == "Code Doubt" and not user_code.strip():
            st.warning("Paste your code first.")
            st.stop()
        if mode == "Concept Doubt" and not user_question.strip():
            st.warning("Type your doubt first.")
            st.stop()

        # ── Fix 3: Input character limit ──────────────────────────────────────
        MAX_CODE_CHARS    = 3000
        MAX_CONCEPT_CHARS = 500
        if mode == "Code Doubt" and len(user_code) > MAX_CODE_CHARS:
            st.warning(f"⚠️ Your code is too long ({len(user_code)} characters). Please paste a maximum of {MAX_CODE_CHARS} characters so CodeFix can analyse it properly.")
            st.stop()
        if mode == "Concept Doubt" and len(user_question) > MAX_CONCEPT_CHARS:
            st.warning(f"⚠️ Your question is too long ({len(user_question)} characters). Please keep it under {MAX_CONCEPT_CHARS} characters for the best response.")
            st.stop()

        stdout_cap = stderr_cap = ""
        stdout_cap = stderr_cap = ""

        if mode == "Code Doubt":
            with st.spinner("⚙️ Running your code…"):
                stdout_cap, stderr_cap = run_code(user_code, language, mock_input=mock_input_str if mock_input_str.strip() else None)
            prompt = build_code_prompt(language, level, user_code, stdout_cap, stderr_cap)
        else:
            prompt = build_concept_prompt(language, level, user_question)

        with st.spinner("🤖 CodeFix is thinking…"):
            try:
                raw = ask_gemini(prompt)
            except Exception as e:
                st.error(f"Groq error: {e}")
                st.stop()

        sections = parse_sections(raw)
        import random
        req_id = random.randint(10000, 99999)

        entry = {
            "type":     "Code" if mode == "Code Doubt" else "Concept",
            "language": language,
            "level":    level,
            "input":    user_code if mode == "Code Doubt" else user_question,
            "stdout":   stdout_cap,
            "stderr":   stderr_cap,
            "response": raw,
            "time":     datetime.now().strftime("%H:%M"),
        }
        st.session_state.history.append(entry)
        save_history(st.session_state.history)
        st.session_state.breakdown = {
            "mode":     "Code" if mode == "Code Doubt" else "Concept",
            "language": language,
            "level":    level,
            "sections": sections,
            "raw":      raw,
            "stdout":   stdout_cap,
            "stderr":   stderr_cap,
            "req_id":   req_id,
        }

    # ── RESPONSE — shown below input whenever available ───────────────────────
    if st.session_state.breakdown:
        bd   = st.session_state.breakdown
        secs = bd["sections"]

        st.markdown("---")
        st.markdown(f"""
        <div class="breakdown-header">
            <div>
                <span class="bh-badge">✦ AI Analysis Complete &nbsp; Request #{bd['req_id']}</span>
                <div class="bh-title">Response Breakdown</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        lang_map = {"Python": "python", "C": "c", "C++": "cpp"}

        if bd["mode"] == "Code":
            st.markdown('<p style="font-size:0.68rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#34d399;margin-bottom:0.3rem;">📤 Execution Output</p>', unsafe_allow_html=True)
            st.code(bd["stdout"] if bd["stdout"].strip() else "(no output)", language=None)

            st.markdown('<p style="font-size:0.68rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#f87171;margin-bottom:0.3rem;">🚨 Error Captured</p>', unsafe_allow_html=True)
            st.code(bd["stderr"] if bd["stderr"].strip() else "(no errors)", language=None)

            st.markdown("---")

            # ── Fix 2: Show clean-run card if no errors ───────────────────────
            code_ran_clean = not bd["stderr"].strip()
            if code_ran_clean:
                st.markdown(f'''
                <div class="resp-card card-fix">
                    <div class="rc-head"><span class="rc-icon">✅</span><span class="rc-title">Code Ran Successfully</span></div>
                    <div class="rc-body">Your code executed without any errors! CodeFix has reviewed it and provided improvement suggestions below.</div>
                </div>''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="resp-card card-error">
                    <div class="rc-head"><span class="rc-icon">🔴</span><span class="rc-title">Error Diagnosis</span></div>
                    <div class="rc-body">{secs.get("Error Diagnosis","—")}</div>
                </div>''', unsafe_allow_html=True)

            if not code_ran_clean:
                st.markdown(f'''
                <div class="resp-card card-why">
                    <div class="rc-head"><span class="rc-icon">🔍</span><span class="rc-title">Why This Happened</span></div>
                    <div class="rc-body">{secs.get("Why This Happened","—")}</div>
                </div>''', unsafe_allow_html=True)

            st.markdown('''
            <div class="resp-card card-fix">
                <div class="rc-head"><span class="rc-icon">✅</span><span class="rc-title">Fixed Code</span></div>
            </div>''', unsafe_allow_html=True)
            st.code(secs.get("Fixed Code",""), language=lang_map.get(bd["language"],"python"))

            st.markdown(f'''
            <div class="resp-card card-improve">
                <div class="rc-head"><span class="rc-icon">📈</span><span class="rc-title">Code Improvement</span></div>
                <div class="rc-body">{secs.get("Code Improvement","—")}</div>
            </div>''', unsafe_allow_html=True)

            st.markdown(f'''
            <div class="resp-card card-remember">
                <div class="rc-head"><span class="rc-icon">📌</span><span class="rc-title">Remember This</span></div>
                <div class="rc-body" style="color:#c4b5fd;font-style:italic;">"{secs.get("Remember This","—")}"</div>
            </div>''', unsafe_allow_html=True)

        else:
            st.markdown(f'''
            <div class="resp-card card-error">
                <div class="rc-head"><span class="rc-icon">💡</span><span class="rc-title">Concept Explanation</span></div>
                <div class="rc-body" style="font-size:1rem;line-height:1.8;">{secs.get("Concept Explanation","—")}</div>
            </div>''', unsafe_allow_html=True)

            st.markdown('''
            <div class="resp-card card-fix">
                <div class="rc-head"><span class="rc-icon">💻</span><span class="rc-title">Example</span></div>
            </div>''', unsafe_allow_html=True)
            st.code(secs.get("Example",""), language=lang_map.get(bd["language"],"python"))

            st.markdown(f'''
            <div class="resp-card card-why">
                <div class="rc-head"><span class="rc-icon">🌍</span><span class="rc-title">Real-World Analogy</span></div>
                <div class="rc-body" style="font-size:1rem;line-height:1.8;">{secs.get("Real-World Analogy","—")}</div>
            </div>''', unsafe_allow_html=True)

            st.markdown(f'''
            <div class="resp-card card-remember">
                <div class="rc-head"><span class="rc-icon">📌</span><span class="rc-title">Remember This</span></div>
                <div class="rc-body" style="color:#c4b5fd;font-style:italic;">"{secs.get("Remember This","—")}"</div>
            </div>''', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  HISTORY TAB (full view)
# ════════════════════════════════════════════════════════════════════════════
with tab_history:
    if not st.session_state.history:
        st.markdown("""
        <div style="text-align:center;padding:4rem 0;color:#475569;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">📚</div>
            <div style="font-size:1rem;font-weight:600;color:#64748b;">No doubts solved yet</div>
            <div style="font-size:0.8rem;margin-top:0.3rem;">Head to the Solve tab to get started</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        fh = st.radio(
            "Filter history", ["All", "Code", "Concept"],
            horizontal=True, label_visibility="collapsed"
        )
        pool = [h for h in reversed(st.session_state.history)
                if fh == "All" or h["type"] == fh]

        st.markdown(f"<p style='font-size:0.75rem;color:#475569;margin:0.5rem 0 1rem;'>{len(pool)} doubt(s)</p>", unsafe_allow_html=True)

        for i, entry in enumerate(pool):
            icon = "💻" if entry["type"] == "Code" else "💡"
            header = (entry["input"][:55] + "…") if len(entry["input"]) > 55 else entry["input"]
            with st.expander(f"{icon} [{entry['language']} · {entry['level']}]  {header}  ·  {entry['time']}"):
                if entry["type"] == "Code":
                    st.markdown("**Your Code:**")
                    st.code(entry["input"], language=entry["language"].lower())
                    c1, c2 = st.columns(2)
                    with c1:
                        if entry.get("stdout"):
                            st.markdown("**Output:**")
                            st.code(entry["stdout"], language=None)
                    with c2:
                        if entry.get("stderr"):
                            st.markdown("**Error:**")
                            st.code(entry["stderr"], language=None)
                else:
                    st.markdown(f"**Doubt:** _{entry['input']}_")
                st.markdown("---")
                st.markdown("**CodeFix Response:**")
                st.markdown(entry["response"])
