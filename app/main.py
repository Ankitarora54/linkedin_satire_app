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

st.set_page_config(page_title="LinkedIn Satire Generator", layout="wide")
# ---------- LOAD EXTERNAL CSS ----------
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------- LOAD PROMPTS FROM FILE ----------
def load_prompt(template_name):
    with open("prompts.txt", "r") as f:
        content = f.read()

    sections = content.split("###")

    for section in sections:
        if section.strip().startswith(template_name):
            return section.replace(template_name, "").strip()

    return ""


st.markdown(
    "<h2 style='text-align: center;'>LinkedIn Satire Generator → Decoder</h2>",
    unsafe_allow_html=True
)

# ---------- MODE ----------
mode = st.radio("",["Reality → LinkedIn", "LinkedIn → Reality"],index=1,horizontal=True)


# ---------- MODE SWITCHING SESSION STATE ----------
if "prev_mode" not in st.session_state:
    st.session_state.prev_mode = mode

if st.session_state.prev_mode != mode:
    st.session_state.output = ""
    st.session_state.prev_mode = mode

# ---------- SESSION ----------
if "output" not in st.session_state:
    st.session_state.output = ""
    st.session_state.exaggeration = 1

# ---------- LAYOUT ----------
col1, col2 = st.columns([1, 2])


# ---------- FORWARD ----------
if mode == "Reality → LinkedIn":

    with col1:
        loader_placeholder = st.empty()
        st.markdown("<h6>Your Reality</h6>", unsafe_allow_html=True)
        user_input = st.text_area("Write any reality you'd like to transform. plain simple language. The funnier the better!!!",height=250)

        tone = st.selectbox("Tone", [
            "Corporate Influencer",
            "Humble Brag",
            "Spiritual Guru",
            "Startup Founder"
        ])

        spice = st.slider("Cringe Level", 1, 5, 3)

        if st.button("Translate →"):
            if user_input.strip():
                base_prompt = load_prompt("FORWARD")
                st.session_state.loading = True
                st.session_state.output = ""
                loader_html="""
                    <div class="loader">
                        <div class="dot-loader">
                            <div class="dot"></div>
                            <div class="dot"></div>
                            <div class="dot"></div>
                        </div>
                        <div class="loader-text">Translating your thoughts into corporate wisdom...</div>
                    </div>
                    """
                loader_placeholder.markdown(loader_html, unsafe_allow_html=True)
                prompt = base_prompt.format(
                    input=user_input,
                    tone=tone,
                    spice=spice,
                    exaggeration=1
                )

                response = client.chat.completions.create(
                    model="gpt-5-mini", #"gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                    #temperature=0.9
                )

                st.session_state.output = response.choices[0].message.content
                st.session_state.loading = False
                loader_placeholder.empty()

    with col2:

        if st.session_state.output:
            st.markdown("<h6>LinkedIn Post</h6>", unsafe_allow_html=True)
            st.markdown(f"<div class='output-box'>{st.session_state.output}</div>", unsafe_allow_html=True)
            output_placeholder = st.empty()

# ---------- REVERSE ----------
else:
    col1, col2 = st.columns([1, 1])
    with col1:
        loader_placeholder = st.empty()
        user_input = st.text_area("**Paste LinkedIn Post**", height=300)
        st.markdown("Paste any LinkedIn post above. It will decode the Author's true emotion behind the post!!!", unsafe_allow_html=True)

        if st.button("Decode →"):
            if user_input.strip():
                base_prompt = load_prompt("REVERSE")
                st.session_state.loading = True
                st.session_state.output = ""
                loader_html="""
                    <div class="loader">
                        <div class="dot-loader">
                            <div class="dot"></div>
                            <div class="dot"></div>
                            <div class="dot"></div>
                        </div>
                        <div class="loader-text">Translating corporate wisdom into reality</div>
                    </div>
                    """
                loader_placeholder.markdown(loader_html, unsafe_allow_html=True)

                prompt = base_prompt.format(input=user_input)
                response = client.chat.completions.create(
                    model="gpt-5-mini", #"gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                    
                    #temperature=0.9
                )

                st.session_state.output = response.choices[0].message.content
                st.session_state.loading = False
                loader_placeholder.empty()

    with col2:
        if st.session_state.output:
            st.markdown("<h6>Decoded Real Emotion</h6>", unsafe_allow_html=True)
            output_placeholder = st.empty()
            st.markdown(f"<div class='output-box'>{st.session_state.output}</div>", unsafe_allow_html=True)


# ---------- FOOTER ----------
st.markdown("---")
st.caption("Prompt-driven AI app by [Ankit Arora] • Powered by OpenAI's GPT-5.1")