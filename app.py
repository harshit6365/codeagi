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
    .stApp { background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%); color: #ffffff; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d0d1a 0%, #1a1a2e 100%); border-right: 1px solid #00d4ff33; }
    .codeagi-card { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border: 1px solid #00d4ff33; border-radius: 16px; padding: 24px; margin: 12px 0; box-shadow: 0 4px 24px rgba(0,212,255,0.1); }
    .codeagi-title { font-size: 2.5rem; font-weight: 700; background: linear-gradient(90deg, #00d4ff, #7b2fff, #00d4ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 8px; }
    .codeagi-subtitle { text-align: center; color: #888; font-size: 0.95rem; margin-bottom: 24px; }
    .stButton > button { background: linear-gradient(90deg, #00d4ff, #7b2fff); color: white; border: none; border-radius: 12px; padding: 12px 28px; font-weight: 600; width: 100%; box-shadow: 0 4px 15px rgba(0,212,255,0.3); }
    .stTextArea > div > div > textarea { background: #0d0d1a; border: 1px solid #00d4ff33; border-radius: 12px; color: #00d4ff; font-family: 'Courier New', monospace; }
    .metric-card { background: linear-gradient(135deg, #1a1a2e, #16213e); border: 1px solid #00d4ff33; border-radius: 12px; padding: 16px; text-align: center; margin-bottom: 8px; }
    .metric-num { font-size: 2rem; font-weight: 700; color: #00d4ff; }
    .metric-label { font-size: 0.8rem; color: #888; margin-top: 4px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0;'>
        <div style='font-size:2.5rem'>🧠</div>
        <div style='font-size:1.3rem; font-weight:700; background: linear-gradient(90deg, #00d4ff, #7b2fff); -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>CodeAGI</div>
        <div style='font-size:0.75rem; color:#888; margin-top:4px;'>by harnartech</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    pages = ["🏠 Home", "🐛 Bug Finder", "⚡ Code Runner", "🛠 Code Fixer", "🤖 Prototype Builder"]
    selected = st.radio("", pages, index=pages.index(st.session_state.current_page))
    st.session_state.current_page = selected

    st.divider()
    st.markdown("<div style='text-align:center; color:#888; font-size:0.75rem;'>AGI-powered Code Intelligence<br>Built with ❤️ in Jaipur, India</div>", unsafe_allow_html=True)

page = st.session_state.current_page

if page == "🏠 Home":
    st.markdown('<div class="codeagi-title">🧠 CodeAGI</div>', unsafe_allow_html=True)
    st.markdown('<div class="codeagi-subtitle">AGI-powered Code Intelligence — Find bugs, fix code, run programs, build prototypes</div>', unsafe_allow_html=True)
    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-card"><div class="metric-num">🐛</div><div style="font-size:1rem;font-weight:600;color:white;margin-top:8px;">Bug Finder</div><div class="metric-label">Find every bug instantly</div></div>', unsafe_allow_html=True)
        if st.button("Open Bug Finder →", key="btn_bug"):
            st.session_state.current_page = "🐛 Bug Finder"
            st.rerun()

    with col2:
        st.markdown('<div class="metric-card"><div class="metric-num">⚡</div><div style="font-size:1rem;font-weight:600;color:white;margin-top:8px;">Code Runner</div><div class="metric-label">Run & debug live</div></div>', unsafe_allow_html=True)
        if st.button("Open Code Runner →", key="btn_run"):
            st.session_state.current_page = "⚡ Code Runner"
            st.rerun()

    with col3:
        st.markdown('<div class="metric-card"><div class="metric-num">🛠</div><div style="font-size:1rem;font-weight:600;color:white;margin-top:8px;">Code Fixer</div><div class="metric-label">Fix broken code</div></div>', unsafe_allow_html=True)
        if st.button("Open Code Fixer →", key="btn_fix"):
            st.session_state.current_page = "🛠 Code Fixer"
            st.rerun()

    with col4:
        st.markdown('<div class="metric-card"><div class="metric-num">🤖</div><div style="font-size:1rem;font-weight:600;color:white;margin-top:8px;">Prototype Builder</div><div class="metric-label">Build from description</div></div>', unsafe_allow_html=True)
        if st.button("Open Prototype Builder →", key="btn_proto"):
            st.session_state.current_page = "🤖 Prototype Builder"
            st.rerun()

    st.divider()
    st.markdown("""
    <div class="codeagi-card">
        <h3 style='color:#00d4ff; margin-bottom:12px;'>🚀 What is CodeAGI?</h3>
        <p style='color:#aaa; line-height:1.8;'>
        CodeAGI is an AGI-powered code intelligence tool built for developers.
        It uses advanced AI to find bugs, explain errors, fix broken code,
        run Python programs live, and build working prototypes from plain English.
        </p>
        <p style='color:#aaa; line-height:1.8; margin-top:12px;'>
        Built by <strong style='color:#00d4ff;'>harnartech</strong> from Jaipur, India.
        Part of the Vision7Lab ecosystem.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif page == "🐛 Bug Finder":
    st.markdown('<div class="codeagi-title">🐛 Bug Finder</div>', unsafe_allow_html=True)
    st.markdown('<div class="codeagi-subtitle">Paste your code — CodeAGI finds every bug instantly</div>', unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns([3, 1])
    with col1:
        code_input = st.text_area("Paste your code here", height=300, placeholder="Paste your code here...")
    with col2:
        language = st.selectbox("Language", ["Python", "JavaScript", "Java", "C++", "HTML/CSS"])
        st.markdown("<br>", unsafe_allow_html=True)
        find_bugs = st.button("Find Bugs 🐛")

    if find_bugs:
        if not code_input:
            st.error("Please paste some code first!")
        else:
            prompt = f"""
            You are a senior {language} developer and code reviewer.
            Analyze this code and find ALL bugs, errors, and issues.
            For each bug: line number, bug type, explanation, fixed code, why fix works.
            Also give: code quality score out of 10, top 3 improvements.
            Code: ```{language}\n{code_input}\n```
            """
            with st.spinner("🧠 CodeAGI is analyzing your code..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
            st.success("✅ Analysis Complete!")
            st.divider()
            st.markdown(result)

elif page == "⚡ Code Runner":
    st.markdown('<div class="codeagi-title">⚡ Code Runner</div>', unsafe_allow_html=True)
    st.markdown('<div class="codeagi-subtitle">Run Python code live — errors explained by AI</div>', unsafe_allow_html=True)
    st.divider()

    code_input = st.text_area("Write or paste Python code", height=300, placeholder="print('Hello CodeAGI!')")
    run_btn = st.button("Run Code ⚡")

    if run_btn:
        if not code_input:
            st.error("Please write some code first!")
        else:
            with st.spinner("Running your code..."):
                try:
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                        f.write(code_input)
                        temp_file = f.name

                    result = subprocess.run(["python", temp_file], capture_output=True, text=True, timeout=10)

                    if result.returncode == 0:
                        st.success("✅ Code ran successfully!")
                        st.subheader("Output:")
                        st.code(result.stdout)
                    else:
                        st.error("❌ Error found!")
                        st.code(result.stderr)
                        explain_prompt = f"Python error:\nCode: {code_input}\nError: {result.stderr}\nExplain: what caused it, exact fix, how to avoid."
                        with st.spinner("🧠 Explaining error..."):
                            error_response = client.chat.completions.create(
                                model="llama-3.3-70b-versatile",
                                messages=[{"role": "user", "content": explain_prompt}]
                            )
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
    st.markdown('<div class="codeagi-title">🛠 Code Fixer</div>', unsafe_allow_html=True)
    st.markdown('<div class="codeagi-subtitle">Paste broken code — get fixed code instantly</div>', unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns([3, 1])
    with col1:
        broken_code = st.text_area("Paste your broken code", height=250, placeholder="Paste broken code here...")
        problem_desc = st.text_input("Describe the problem (optional)", placeholder="e.g. Getting TypeError on line 5")
    with col2:
        language = st.selectbox("Language", ["Python", "JavaScript", "Java", "C++", "HTML/CSS"])
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        fix_btn = st.button("Fix My Code 🛠")

    if fix_btn:
        if not broken_code:
            st.error("Please paste your code first!")
        else:
            prompt = f"Fix this broken {language} code.\nCode: {broken_code}\nProblem: {problem_desc if problem_desc else 'Not provided'}\nProvide: fixed complete code, all changes made, why each fix was needed."
            with st.spinner("🧠 Fixing your code..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                fixed = response.choices[0].message.content
            st.success("✅ Code Fixed!")
            st.divider()
            st.markdown(fixed)
            st.download_button("📥 Download Fixed Code", data=fixed, file_name="fixed_code.txt", mime="text/plain")

elif page == "🤖 Prototype Builder":
    st.markdown('<div class="codeagi-title">🤖 Prototype Builder</div>', unsafe_allow_html=True)
    st.markdown('<div class="codeagi-subtitle">Describe what you want — CodeAGI writes the code</div>', unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns([3, 1])
    with col1:
        description = st.text_area("Describe what you want to build", height=150, placeholder="e.g. A Python script that reads CSV, removes duplicates, saves clean version")
    with col2:
        language = st.selectbox("Language", ["Python", "JavaScript", "HTML/CSS", "SQL", "Bash"])
        complexity = st.select_slider("Complexity", options=["Beginner", "Intermediate", "Advanced"])
        build_btn = st.button("Build Prototype 🤖")

    if build_btn:
        if not description:
            st.error("Please describe what you want!")
        else:
            prompt = f"Build a complete {language} prototype.\nDescription: {description}\nComplexity: {complexity}\nProvide: complete working code with comments, how to run it, what to add next."
            with st.spinner("🧠 Building your prototype..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                prototype = response.choices[0].message.content
            st.success("✅ Prototype Ready!")
            st.divider()
            st.markdown(prototype)
            st.download_button("📥 Download Code", data=prototype, file_name="prototype.txt", mime="text/plain")