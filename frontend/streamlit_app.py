import streamlit as st
import requests
from typing import Optional

st.set_page_config(page_title="Help Assistant", page_icon="💬", layout="wide")

st.markdown(
    """
    <style>
        :root {
            color-scheme: dark;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(52, 211, 153, 0.14), transparent 30%),
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.16), transparent 28%),
                linear-gradient(180deg, #0a0f1a 0%, #0f172a 100%);
            color: #e5e7eb;
        }

        .block-container {
            max-width: 980px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .hero-card {
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 24px;
            padding: 1.5rem 1.5rem 1.25rem;
            background: rgba(15, 23, 42, 0.72);
            box-shadow: 0 18px 60px rgba(2, 6, 23, 0.45);
            backdrop-filter: blur(16px);
            margin-bottom: 1rem;
        }

        .hero-title {
            font-size: 2.1rem;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 0.35rem;
        }

        .hero-subtitle {
            color: #cbd5e1;
            font-size: 1rem;
            line-height: 1.6;
        }

        .chat-wrap {
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 24px;
            background: rgba(2, 6, 23, 0.55);
            box-shadow: 0 18px 60px rgba(2, 6, 23, 0.35);
            padding: 1rem;
        }

        .bubble {
            border-radius: 18px;
            padding: 0.95rem 1rem;
            margin: 0.65rem 0;
            line-height: 1.55;
            width:100%
            white-space: pre-wrap;
        }

        .bubble.user {
            width:100%
            margin-left: auto;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: #f8fafc;
            box-shadow: 0 10px 24px rgba(37, 99, 235, 0.25);
        }

        .bubble.support {
            width:100%
            background: rgba(15, 23, 42, 0.92);
            color: #e2e8f0;
            border: 1px solid rgba(148, 163, 184, 0.16);
        }

        .bubble-meta {
            display: block;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            opacity: 0.72;
            margin-bottom: 0.35rem;
        }

        .stTextArea textarea {
            background: rgba(15, 23, 42, 0.92) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(148, 163, 184, 0.28) !important;
            border-radius: 16px !important;
            min-height: 130px !important;
        }

        .stButton button {
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
            color: white;
            border: none;
            border-radius: 14px;
            padding: 0.65rem 1rem;
            font-weight: 700;
            width: 100%;
        }

        .stButton button:hover {
            filter: brightness(1.03);
            transform: translateY(-1px);
        }

        .sidebar-card {
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 18px;
            padding: 1rem;
            background: rgba(15, 23, 42, 0.72);
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Backend endpoint placeholder: set this to your support endpoint, e.g.
# http://127.0.0.1:8000/support
BACKEND_ENDPOINT: Optional[str] = "http://127.0.0.1:8000/user_query"  # leave empty to use local canned replies


def send_to_backend(message: str) -> str:
    """Send message to backend endpoint if configured, otherwise return empty string.

    The function returns the backend reply text on success, or an error message
    describing the failure. If `BACKEND_ENDPOINT` is empty, this returns an empty
    string so the UI can fall back to a canned reply.
    """
    if not BACKEND_ENDPOINT:
        return ""
    try:
        payload={
            "query": message
        }
        resp = requests.post(BACKEND_ENDPOINT, json=payload,)
        resp.raise_for_status()
        data = resp.json()
        return str(data)
    except Exception as e:
        return f"(backend error) {e}"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "support",
            "text": "Welcome to Help Assistant. Tell me what is broken, what you expected, and any error message you saw.",
        }
    ]



st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">Help Assistant</div>
        <div class="hero-subtitle">
            A clean dark support chat for users to describe complaints, share details,
            and get guided help without the clutter.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left = st.container()

with left:
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        role_class = "user" if message["role"] == "user" else "support"
        label = "You" if message["role"] == "user" else "Support"
        st.markdown(
            f"""
            <div class="bubble {role_class}">
                <span class="bubble-meta">{label}</span>
                {message['text']}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.form("chat_form", clear_on_submit=True):
        user_message = st.text_area(
            "Describe your issue",
            placeholder="Example: I cannot log in even after resetting my password.",
            label_visibility="collapsed",
        )
        send = st.form_submit_button("Send message")

    if send and user_message.strip():
        st.session_state.messages.append({"role": "user", "text": user_message.strip()})
        # First try backend if configured
        backend_reply = send_to_backend(user_message.strip())
        if backend_reply:
            st.session_state.messages.append({"role": "support", "text": backend_reply})
        else:
            # fallback canned reply when no backend is configured or it failed
            support_reply = (
                "Thanks for the report. Please share any error message, the exact steps you took, and when it started. "
                "I’ll help narrow it down."
            )
            st.session_state.messages.append({"role": "support", "text": support_reply})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)