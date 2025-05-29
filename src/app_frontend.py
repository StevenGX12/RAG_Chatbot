import streamlit as st
import requests
from streamlit_chat import message

API_URL = "http://localhost:8000/chat"
BOT_PROFILE_IMAGE = (
    "https://res.cloudinary.com/webmonc/image/upload/v1696515089/3558860_r0hs4y.png"
)
USER_PROFILE_IMAGE = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/a0a7586b-3d38-4293-9d13-75e10782ff57/dgsxyf3-9950af01-ba44-4113-9bb0-c34a83359217.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2EwYTc1ODZiLTNkMzgtNDI5My05ZDEzLTc1ZTEwNzgyZmY1N1wvZGdzeHlmMy05OTUwYWYwMS1iYTQ0LTQxMTMtOWJiMC1jMzRhODMzNTkyMTcucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.oVZe6OpHCSGmpZ34O2yP6Kv5V8USfdAFQMlaI4WDKAc"

st.set_page_config(page_title="Interview Prep Chatbot", page_icon="🧠")
st.markdown(
    "<h2 style='text-align:center;'>🧠 Technical Interview Chatbot</h2>",
    unsafe_allow_html=True,
)

# --- CSS Styling ---
st.markdown(
    """
<style>
/* Hide default Streamlit elements */
#MainMenu, header, footer {visibility: hidden;}

/* Make textarea auto-resize */
textarea {
    overflow-y: auto;
    resize: none;
    min-height: 40px;
    max-height: 200px;
    line-height: 1.4;
    padding: 10px;
    font-size: 1rem;
    background-color: #262730;
    color: white;
    border-radius: 8px;
    border: 1px solid #444;
}

/* Remove red outline on focus */
textarea:focus {
    border: 1px solid #888 !important;
    outline: none !important;
    box-shadow: none !important;
}


/* Fixed input bar aligned with chat */
.stForm {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1rem 1rem 0.5rem 1rem;
    z-index: 999;
    display: flex;
    justify-content: center;
    border-style: none;
}

/* Constrain form input width */
.stForm > div {
    max-width: 800px;
    width: 100%;
}

.chat-wrapper {
    max-width: 1000px;
    margin: 0 auto;
    padding: 1rem;
}


</style>
""",
    unsafe_allow_html=True,
)


# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thinking" not in st.session_state:
    st.session_state.thinking = False

# --- Chat Display (in scrollable container) ---
with st.container():
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

    for i, msg in enumerate(st.session_state.messages):
        message(
            msg["query"],
            is_user=True,
            key=f"user_{i}",
            avatar_style="initials",
            logo=USER_PROFILE_IMAGE,
        )
        if msg["answer"] == "__thinking__":
            message(
                "Thinking...",
                key=f"thinking_{i}",
                avatar_style="bottts",
                logo=BOT_PROFILE_IMAGE,
            )
        else:
            message(
                msg["answer"],
                key=f"bot_{i}",
                avatar_style="bottts",
                logo=BOT_PROFILE_IMAGE,
            )

    st.markdown("</div>", unsafe_allow_html=True)


# --- Handle Form Submission (fixed input) ---
with st.form("chat_form", clear_on_submit=True):
    query = st.text_area(
        "You:",
        key="input",
        height=120,
        label_visibility="collapsed",
        placeholder="Type your question...",
    )

    col1, col2 = st.columns([6, 1])
    with col1:
        st.text("")  # Empty space to align button
    with col2:
        submitted = st.form_submit_button("Send", use_container_width=True)


# --- Append new user message + thinking placeholder ---
if submitted and query:
    st.session_state.messages.append({"query": query, "answer": "__thinking__"})
    st.session_state.thinking = True
    st.rerun()

# --- Replace placeholder with real answer ---
if st.session_state.thinking:
    last_index = len(st.session_state.messages) - 1
    last_query = st.session_state.messages[last_index]["query"]

    with st.spinner("Thinking..."):
        response = requests.post(API_URL, json={"query": last_query})
        answer = response.json()["answer"]

    st.session_state.messages[last_index]["answer"] = answer
    st.session_state.thinking = False
    st.rerun()
