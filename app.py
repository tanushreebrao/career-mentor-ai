import streamlit as st
from resume_parser import extract_text_from_pdf
from llm import analyze_resume
from memory import save_memory, get_memory

# ================== CONFIG ==================
st.set_page_config(page_title="CareerMind AI", page_icon="🚀", layout="wide")

# ================== SESSION ==================
if "result" not in st.session_state:
    st.session_state.result = ""
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

# ================== DARK MODE ==================
mode = st.toggle("🌙 Dark Mode")

# ================== COLORS ==================
if mode:
    bg = "#1E293B"
    text = "#F8FAFC"
    card = "#334155"
    primary = "#3B82F6"
    secondary = "#14B8A6"
else:
    bg = "#F5F7FB"
    text = "#1F2937"
    card = "#FFFFFF"
    primary = "#2563EB"
    secondary = "#0EA5E9"

# ================== CSS ==================
st.markdown(f"""
<style>
.stApp {{
    background-color: {bg};
    color: {text};
}}

h1 {{
    font-size: 42px !important;
    font-weight: 700;
}}

h3 {{
    font-size: 22px !important;
}}

label, .stMarkdown {{
    font-size: 18px !important;
}}

input {{
    font-size: 18px !important;
    padding: 12px !important;
}}

.stTextInput>div>div>input {{
    background-color: {"#334155" if mode else "white"};
    color: {"#E2E8F0" if mode else "#1F2937"};
    border-radius: 10px;
}}

.stFileUploader {{
    background-color: white !important;
    color: black !important;
    padding: 15px;
    border-radius: 10px;
}}

.stFileUploader * {{
    color: black !important;
}}

.stButton>button {{
    background-color: {primary};
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 220px;
    font-size: 18px;
    font-weight: 600;
}}

.card {{
    background-color: {card};
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    border-left: 6px solid {primary};
}}

.card-title {{
    color: {primary};
    font-size: 24px;
    font-weight: bold;
}}

.card-sub {{
    color: {secondary};
    font-size: 16px;
    margin-bottom: 10px;
}}

.card-text {{
    font-size: 18px;
    line-height: 1.6;
}}
</style>
""", unsafe_allow_html=True)

# ================== TITLE ==================
st.title("🚀 CareerMind AI")
st.markdown("### A self-learning career mentor with memory")

# ================== INPUT ==================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👤 User ID")
    user_id = st.text_input("", placeholder="Enter your user ID")

with col2:
    st.markdown("### 💼 Job Role")
    job_role = st.text_input("", placeholder="Enter job role")

st.markdown("### 📄 Upload Resume")
uploaded_file = st.file_uploader("", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# ================== SPLIT FUNCTION ==================
def split_sections(text):
    sections = {"Skill Gaps": "", "Suggestions": "", "Improvements": ""}
    current = None

    for line in text.split("\n"):
        line = line.strip()

        if "Skill Gaps" in line:
            current = "Skill Gaps"
            continue
        elif "Suggestions" in line:
            current = "Suggestions"
            continue
        elif "Improvements" in line:
            current = "Improvements"
            continue

        if current:
            sections[current] += line + "<br>"

    return sections

# ================== ANALYZE ==================
if st.button("🚀 Analyze Resume"):
    if uploaded_file and user_id and job_role:

        resume_text = extract_text_from_pdf(uploaded_file)
        past_memory = get_memory(user_id)

        with st.spinner("Analyzing..."):
            result = analyze_resume(resume_text, job_role, past_memory)

        st.session_state.result = result
        st.session_state.analyzed = True

        summary = f"Skills: {job_role}\n{result[:150]}"
        save_memory(user_id, job_role, summary)

    else:
        st.warning("Please fill all fields")

# ================== SHOW RESULT ==================
if st.session_state.result:

    sections = split_sections(st.session_state.result)

    st.markdown("## 📊 AI Analysis")

    st.markdown(f"""
    <div class="card">
        <div class="card-title">🔴 Skill Gaps</div>
        <div class="card-sub">What you're missing</div>
        <div class="card-text">{sections["Skill Gaps"]}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <div class="card-title">🟡 Suggestions</div>
        <div class="card-sub">What you should do</div>
        <div class="card-text">{sections["Suggestions"]}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <div class="card-title">🟢 Improvements</div>
        <div class="card-sub">How to improve</div>
        <div class="card-text">{sections["Improvements"]}</div>
    </div>
    """, unsafe_allow_html=True)

# ================== MEMORY ==================
past_data = get_memory(user_id)

if past_data:
    st.markdown("---")
    st.markdown("## 🧠 Previous Attempts")

    for i, entry in enumerate(past_data):
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Attempt {i+1} — {entry['job_role']}</div>
            <div class="card-text">{entry['result'][:200]}...</div>
        </div>
        """, unsafe_allow_html=True)

# ================== LEARNING ==================
st.markdown("---")
st.markdown("## 🚀 Learning Insight")

attempt_count = len(past_data)

if attempt_count >= 2:
    st.success("Your profile is improving based on previous attempts 🚀")
elif st.session_state.analyzed:
    st.warning("First attempt — no prior memory yet")

# ================== SCORE ==================

def calculate_score(result_text):
    score = 100

    penalties = [
        "no mention",
        "lack of",
        "absence of",
        "missing",
        "limited"
    ]

    text = result_text.lower()
    penalty_count = sum(text.count(p) for p in penalties)

    score -= penalty_count * 10

    return max(20, min(100, score))


if st.session_state.analyzed:

    score = calculate_score(st.session_state.result)

    st.markdown("## 📊 Confidence Score")

    st.markdown(f"""
    <div style="
        background: linear-gradient(to right, red, orange, yellow, green);
        border-radius: 20px;
        height: 20px;
        position: relative;
    ">
        <div style="
            position: absolute;
            left: {score}%;
            top: -5px;
            width: 0;
            height: 0;
            border-left: 8px solid transparent;
            border-right: 8px solid transparent;
            border-top: 12px solid black;
        "></div>
    </div>

    <p style="margin-top:10px;"><b>{score}/100</b></p>
    """, unsafe_allow_html=True)