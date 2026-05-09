import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import subprocess
import tempfile

load_dotenv()
API_KEY = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=API_KEY)

st.set_page_config(page_title="CodeAGI", page_icon="🧠", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #050510; color: #ffffff; }
[data-testid="stSidebar"] { background: #0a0a1a; border-right: 1px solid #ffffff10; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

/* Make button look like a card */
.stButton > button {
    background: linear-gradient(135deg, #0d0d2a, #1a1a3e) !important;
    color: white !important;
    border: 1px solid #ffffff10 !important;
    border-radius: 20px !important;
    padding: 40px 24px !important;
    font-weight: 600 !important;
    width: 100% !important;
    height: 200px !important;
    font-size: 1rem !important;
    line-height: 2.2 !important;
    box-shadow: 0 4px 24px rgba(0,212,255,0.08) !important;
    transition: all 0.3s ease !important;
    white-space: pre-line !important;
    letter-spacing: 0.3px !important;
    text-shadow: 0 0 20px rgba(0,212,255,0.5) !important;
}
            
.stButton > button:hover {
    border-color: #00d4ff40 !important;
    transform: translateY(-4px) !important;
    box-shadow: 0 20px 60px rgba(0,212,255,0.15) !important;
    background: linear-gradient(135deg, #0d0d2a, #1a1a3e) !important;
}

/* Back button different style */
.back-btn .stButton > button {
    background: #ffffff10 !important;
    border: 1px solid #ffffff20 !important;
    border-radius: 10px !important;
    padding: 8px 16px !important;
    font-size: 0.85rem !important;
    width: auto !important;
    height: auto !important;
    color: #ffffff80 !important;
    box-shadow: none !important;
}

.hero-title { font-size: 3.5rem; font-weight: 800; background: linear-gradient(135deg, #00d4ff 0%, #7b2fff 50%, #ff006e 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; line-height: 1.1; margin-bottom: 16px; }
.hero-sub { text-align: center; color: #ffffff50; font-size: 1.1rem; margin-bottom: 48px; font-weight: 300; }
.page-title { font-size: 2rem; font-weight: 700; background: linear-gradient(90deg, #00d4ff, #7b2fff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 6px; }
.page-sub { color: #ffffff40; font-size: 0.9rem; margin-bottom: 24px; }
.stats-bar { display: flex; gap: 24px; justify-content: center; margin: 32px 0; flex-wrap: wrap; }
.stat { text-align: center; }
.stat-num { font-size: 2rem; font-weight: 700; background: linear-gradient(90deg, #00d4ff, #7b2fff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: block; }
.stat-label { font-size: 0.75rem; color: #ffffff30; text-transform: uppercase; letter-spacing: 1px; }
.about-card { background: linear-gradient(135deg, #0d0d2a, #1a1a3e); border: 1px solid #ffffff10; border-radius: 20px; padding: 32px; margin-top: 32px; }
.stTextArea > div > div > textarea { background: #0a0a1a !important; border: 1px solid #ffffff15 !important; border-radius: 12px !important; color: #00d4ff !important; font-family: 'Courier New', monospace !important; }
.stSelectbox > div > div { background: #0a0a1a !important; border: 1px solid #ffffff15 !important; border-radius: 10px !important; color: white !important; }
hr { border-color: #ffffff08 !important; }

/* Action buttons on feature pages */
.stButton > button {
    background: linear-gradient(160deg, #111130 0%, #0d0d2a 60%, #12122e 100%) !important;
    color: #e8f0ff !important;
    border: 1px solid rgba(100, 160, 255, 0.12) !important;
    border-radius: 16px !important;
    padding: 28px 20px !important;
    font-weight: 600 !important;
    width: 100% !important;
    height: 180px !important;
    font-size: 0.95rem !important;
    line-height: 2 !important;
    box-shadow:
        0 2px 0 rgba(255, 255, 255, 0.04) inset,
        0 8px 32px rgba(0, 120, 255, 0.07),
        0 1px 3px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    white-space: pre-line !important;
    letter-spacing: 0.3px !important;
    text-shadow: 0 0 24px rgba(100, 180, 255, 0.35) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    border-radius: 16px !important;
    background: linear-gradient(160deg, rgba(255, 255, 255, 0.04) 0%, transparent 60%) !important;
    pointer-events: none !important;
}

.stButton > button:hover {
    background: linear-gradient(160deg, #161640 0%, #131335 60%, #161640 100%) !important;
    border-color: rgba(100, 180, 255, 0.28) !important;
    box-shadow:
        0 2px 0 rgba(255, 255, 255, 0.06) inset,
        0 12px 40px rgba(0, 140, 255, 0.15),
        0 2px 8px rgba(0, 0, 0, 0.5) !important;
    transform: translateY(-2px) !important;
    color: #ffffff !important;
    text-shadow: 0 0 28px rgba(120, 200, 255, 0.55) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
    box-shadow:
        0 1px 0 rgba(255, 255, 255, 0.03) inset,
        0 4px 16px rgba(0, 100, 255, 0.1),
        0 1px 2px rgba(0, 0, 0, 0.5) !important;
}
</style>
""", unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:30px 0 20px;'>
        <span style='font-size:3rem;display:block;margin-bottom:8px;'>🧠</span>
        <span style='font-size:1.4rem;font-weight:700;background:linear-gradient(90deg,#00d4ff,#7b2fff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;display:block;'>CodeAGI</span>
        <span style='font-size:0.7rem;color:#ffffff40;display:block;margin-top:4px;letter-spacing:2px;text-transform:uppercase;'>by harnartech</span>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    pages = ["🏠 Home","🐛 Bug Finder","⚡ Code Runner","🛠 Code Fixer","🤖 Prototype Builder","🔐 Security Scanner"]
    selected = st.radio("", pages, index=pages.index(st.session_state.current_page))
    st.session_state.current_page = selected
    st.divider()
    st.markdown("<div style='text-align:center;color:#ffffff20;font-size:0.7rem;padding:16px 0;letter-spacing:1px;'>AGI-POWERED CODE INTELLIGENCE<br><br>Built with ❤️ in Jaipur, India</div>", unsafe_allow_html=True)

page = st.session_state.current_page

def back_button():
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.current_page = "🏠 Home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def action_button(label, key):
    st.markdown('<div class="action-btn">', unsafe_allow_html=True)
    clicked = st.button(label, key=key)
    st.markdown('</div>', unsafe_allow_html=True)
    return clicked

if page == "🏠 Home":
    st.markdown('<div class="hero-title">🧠 CodeAGI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">AGI-powered code intelligence. Find bugs, fix code, scan security, build prototypes.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="stats-bar">
        <div class="stat"><span class="stat-num">5</span><span class="stat-label">AI Features</span></div>
        <div class="stat"><span class="stat-num">6+</span><span class="stat-label">Languages</span></div>
        <div class="stat"><span class="stat-num">AGI</span><span class="stat-label">Powered</span></div>
        <div class="stat"><span class="stat-num">Free</span><span class="stat-label">To Use</span></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🐛\n\nBug Finder\n\nFind every bug instantly with line numbers, explanations and fixes", key="h1"):
            st.session_state.current_page = "🐛 Bug Finder"
            st.rerun()

    with col2:
        if st.button("⚡\n\nCode Runner\n\nRun Python code live in browser. Errors explained by AI instantly", key="h2"):
            st.session_state.current_page = "⚡ Code Runner"
            st.rerun()

    with col3:
        if st.button("🛠\n\nCode Fixer\n\nPaste broken code — get fully fixed working code in seconds", key="h3"):
            st.session_state.current_page = "🛠 Code Fixer"
            st.rerun()

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("🤖\n\nPrototype Builder\n\nDescribe what you want in plain English — get working code", key="h4"):
            st.session_state.current_page = "🤖 Prototype Builder"
            st.rerun()

    with col5:
        if st.button("🔐\n\nSecurity Scanner\n\nScan for SQL injection, XSS, hardcoded passwords and more", key="h5"):
            st.session_state.current_page = "🔐 Security Scanner"
            st.rerun()

    with col6:
        st.button("🚀\n\nMore Coming Soon\n\nAI Pair Programmer, Code Reviewer launching soon", key="h6", disabled=True)

    st.markdown("""
    <div class="about-card">
        <h3 style='color:#00d4ff;margin-bottom:12px;font-size:1.1rem;'>About CodeAGI</h3>
        <p style='color:#ffffff50;line-height:1.8;font-size:0.9rem;'>
        CodeAGI is an AGI-powered code intelligence platform built for developers of all levels.
        Uses state-of-the-art AI to analyze, fix, secure, and generate code across multiple languages.
        </p>
        <p style='color:#ffffff50;line-height:1.8;font-size:0.9rem;margin-top:12px;'>
        Built by <strong style='color:#00d4ff;'>harnartech</strong> from Jaipur, India 🇮🇳 — part of the Vision7Lab ecosystem.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif page == "🐛 Bug Finder":
    back_button()
    st.markdown('<div class="page-title">🐛 Bug Finder</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Paste your code — CodeAGI finds every bug instantly</div>', unsafe_allow_html=True)
    st.divider()
    col1, col2 = st.columns([3, 1])
    with col1:
        code_input = st.text_area("Paste your code here", height=300, placeholder="Paste your code here...")
    with col2:
        language = st.selectbox("Language", ["Python", "JavaScript", "Java", "C++", "HTML/CSS"])
        st.markdown("<br>", unsafe_allow_html=True)
        find_bugs = action_button("Find Bugs 🐛", "find_bugs")
    if find_bugs:
        if not code_input:
            st.error("Please paste some code first!")
        else:
            prompt = f"You are a senior {language} developer. Find ALL bugs in this code. For each: line number, type, explanation, fixed code, why fix works. Also: quality score/10, top 3 improvements.\nCode:```{language}\n{code_input}\n```"
            with st.spinner("🧠 Analyzing..."):
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                result = response.choices[0].message.content
            st.success("✅ Analysis Complete!")
            st.divider()
            st.markdown(result)

elif page == "⚡ Code Runner":
    back_button()
    st.markdown('<div class="page-title">⚡ Code Runner</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Run Python code live — errors explained by AI</div>', unsafe_allow_html=True)
    st.divider()
    code_input = st.text_area("Write or paste Python code", height=300, placeholder="print('Hello CodeAGI!')")
    run_btn = action_button("Run Code ⚡", "run_btn")
    if run_btn:
        if not code_input:
            st.error("Please write some code first!")
        else:
            with st.spinner("Running..."):
                try:
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                        f.write(code_input)
                        temp_file = f.name
                    result = subprocess.run(["python", temp_file], capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        st.success("✅ Code ran successfully!")
                        st.code(result.stdout)
                    else:
                        st.error("❌ Error found!")
                        st.code(result.stderr)
                        with st.spinner("🧠 Explaining error..."):
                            error_response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": f"Explain this Python error simply and give fix:\nCode:{code_input}\nError:{result.stderr}"}])
                            st.markdown(error_response.choices[0].message.content)
                except subprocess.TimeoutExpired:
                    st.error("⏱ Timeout — check for infinite loops!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    try:
                        os.unlink(temp_file)
                    except:
                        pass

elif page == "🛠 Code Fixer":
    back_button()
    st.markdown('<div class="page-title">🛠 Code Fixer</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Paste broken code — get fixed code instantly</div>', unsafe_allow_html=True)
    st.divider()
    col1, col2 = st.columns([3, 1])
    with col1:
        broken_code = st.text_area("Paste your broken code", height=250, placeholder="Paste broken code here...")
        problem_desc = st.text_input("Describe the problem (optional)", placeholder="e.g. Getting TypeError on line 5")
    with col2:
        language = st.selectbox("Language", ["Python", "JavaScript", "Java", "C++", "HTML/CSS"])
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        fix_btn = action_button("Fix My Code 🛠", "fix_btn")
    if fix_btn:
        if not broken_code:
            st.error("Please paste your code first!")
        else:
            prompt = f"Fix this broken {language} code completely.\nCode:{broken_code}\nProblem:{problem_desc if problem_desc else 'Not provided'}\nGive: fixed code, all changes made, why each fix was needed."
            with st.spinner("🧠 Fixing..."):
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                fixed = response.choices[0].message.content
            st.success("✅ Code Fixed!")
            st.divider()
            st.markdown(fixed)
            st.download_button("📥 Download Fixed Code", data=fixed, file_name="fixed_code.txt", mime="text/plain")

elif page == "🤖 Prototype Builder":
    back_button()
    st.markdown('<div class="page-title">🤖 Prototype Builder</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Describe what you want — CodeAGI writes the code</div>', unsafe_allow_html=True)
    st.divider()
    col1, col2 = st.columns([3, 1])
    with col1:
        description = st.text_area("Describe what you want to build", height=150, placeholder="e.g. A Python script that reads CSV, removes duplicates, saves clean version")
    with col2:
        language = st.selectbox("Language", ["Python", "JavaScript", "HTML/CSS", "SQL", "Bash"])
        complexity = st.select_slider("Complexity", options=["Beginner", "Intermediate", "Advanced"])
        build_btn = action_button("Build Prototype 🤖", "build_btn")
    if build_btn:
        if not description:
            st.error("Please describe what you want!")
        else:
            prompt = f"Build a complete {language} prototype.\nDescription:{description}\nComplexity:{complexity}\nGive: complete working code with comments, how to run it, what to add next."
            with st.spinner("🧠 Building..."):
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                prototype = response.choices[0].message.content
            st.success("✅ Prototype Ready!")
            st.divider()
            st.markdown(prototype)
            st.download_button("📥 Download Code", data=prototype, file_name="prototype.txt", mime="text/plain")

elif page == "🔐 Security Scanner":
    back_button()
    st.markdown('<div class="page-title">🔐 Security Scanner</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Scan your code for security vulnerabilities</div>', unsafe_allow_html=True)
    st.divider()
    col1, col2 = st.columns([3, 1])
    with col1:
        code_input = st.text_area("Paste your code to scan", height=300, placeholder="Paste your code here...")
    with col2:
        language = st.selectbox("Language", ["Python", "JavaScript", "Java", "PHP", "SQL"])
        scan_type = st.multiselect("Scan for", ["SQL Injection", "XSS", "Hardcoded Passwords", "Insecure API Keys", "Input Validation", "All Vulnerabilities"], default=["All Vulnerabilities"])
        st.markdown("<br>", unsafe_allow_html=True)
        scan_btn = action_button("Scan Code 🔐", "scan_btn")
    if scan_btn:
        if not code_input:
            st.error("Please paste your code first!")
        else:
            prompt = f"You are a cybersecurity expert. Scan this {language} code for: {', '.join(scan_type)}.\nFor each vulnerability: name, severity 🔴HIGH/🟡MEDIUM/🟢LOW, line number, explanation, how attacker exploits, fixed code.\nAlso: security score/10, top 3 improvements.\nCode:```{language}\n{code_input}\n```"
            with st.spinner("🔐 Scanning..."):
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                result = response.choices[0].message.content
            st.success("✅ Security Scan Complete!")
            st.divider()
            st.markdown(result)
            st.download_button("📥 Download Security Report", data=result, file_name="security_report.txt", mime="text/plain")