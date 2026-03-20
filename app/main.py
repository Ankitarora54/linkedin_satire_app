# ==========================================
# LinkedIn Satire AI App (Upgraded UI)
# Features:
# - LinkedIn-style post preview card
# - Cringe Score meter
# - "Make it Worse" button (iterative exaggeration)
# ==========================================

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# ---------- INIT ----------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="LinkedIn Satire Generator", layout="centered")
# ---------- LOAD EXTERNAL CSS ----------
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown(
    "<h1 style='text-align: center;'>LinkedIn Satire Generator</h1>",
    unsafe_allow_html=True
)
#st.title("LinkedIn Satire AI Generator")

# ---------- INPUT ----------
user_input = st.text_area("Enter your moment:")

tone = st.selectbox("Tone", [
    "Corporate Influencer",
    "Humble Brag",
    "Spiritual Guru",
    "Startup Founder"
])

spice = st.slider("Cringe Level", 1, 5, 3)

# ---------- PROMPT ----------
def build_prompt(user_input, tone, spice, exaggeration=1):
    return f"""
You are an AI that converts any user input into a humorous, exaggerated LinkedIn-style post.

Rules:
- NEVER use crude, explicit, or inappropriate words from the input.
- Abstract the situation into a professional or personal growth narrative.
- Use corporate buzzwords, leadership tone, and reflective storytelling.
- Add humor through exaggeration and seriousness.
- Keep it clean and suitable for LinkedIn.
- Do not use the exact words from the input, but capture the essence in a professional and funny way.
- Keep it short in 2-3 lines with a strong hook and clear lessons.
- Include:
  1. Strong opening hook
  2. Story (reframed professionally)
  3. 4–6 relevant hashtags
- Increase exaggeration level: {exaggeration}

Tone: {tone}
Cringe Level: {spice}/5

Structure:
Hook
Story
Lessons
CTA
Hashtags

Make the post feel authentic but unintentionally funny.

Input: {user_input}
"""

# ---------- SESSION STATE ----------
if "output" not in st.session_state:
    st.session_state.output = ""
    st.session_state.exaggeration = 1

# ---------- GENERATE ----------
if st.button("Generate Post"):
    if user_input.strip():
        st.session_state.exaggeration = 1
        prompt = build_prompt(user_input, tone, spice, 1)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )

        st.session_state.output = response.choices[0].message.content

# ---------- MAKE IT WORSE ----------
if st.button("🔥 Make it Worse"):
    if st.session_state.output:
        st.session_state.exaggeration += 1

        prompt = build_prompt(user_input, tone, spice, st.session_state.exaggeration)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0
        )

        st.session_state.output = response.choices[0].message.content

# ---------- CRINGE SCORE ----------
def calculate_cringe(text):
    score = min(100, 40 + len(text.split()) // 3 + text.count("\n") * 2)
    return score

# ---------- OUTPUT ----------
if st.session_state.output:
    cringe_score = calculate_cringe(st.session_state.output)

    st.markdown(f"""
    <div class="card">
        <div class="name">Ankit Arora • AI Enthusiast</div>
        <div class="meta">Just now • 🌍</div>
        <div class="post">{st.session_state.output.replace(chr(10), '<br>')}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="score">🔥 Cringe Score: {cringe_score}/100</div>
    """)

    st.progress(cringe_score / 100)

    #st.code(st.session_state.output)

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Built for maximum LinkedIn drama 🚀")
