import streamlit as st
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

st.set_page_config(
    page_title="Judicial Procedure Information Assistant",
    layout="wide"
)
client = genai.Client(
    api_key=("AIzaSyArNpdjxaDg_ajh2bZ5-zKF_mGjcCczAdM")
)
# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = "gemini-3-flash-preview"
st.markdown("""
    <style>
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .banner {
        background: linear-gradient(135deg,#E6D3B1);
        background-size: 400% 400%;
        animation: gradientMove 12s ease infinite;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        color: brown;
        font-weight: bold;
        font-size: 32px;
        font-family: 'Segoe UI', sans-serif;
        margin-bottom: 20px;
    }
    </style>
    <div class="banner">
        🏛️ Judicial Procedure Information Assistant
    </div>
""", unsafe_allow_html=True)
st.caption(
    "This assistant provides **general procedural information** about courts. "
    "It does **not** give legal advice or case opinions."
)
st.divider()

with st.sidebar:
    st.sidebar.markdown(
    """
    <style>
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .sidebar-banner {
        background: linear-gradient(135deg,#E6D3B1 );
        background-size: 400% 400%;
        animation: gradientMove 12s ease infinite;
        width: 100%;
        padding: 10px 12px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
        text-align: center;
        color: brown;
        font-size: 18px;
        font-weight: bold;
        font-family: Georgia, serif;
        margin-bottom: 15px;
        word-wrap: break-word;
    }
    </style>

    <div class="sidebar-banner">
        About This Assistant
    </div>
    """,
    unsafe_allow_html=True)

    st.write(
        "Explains court procedures, hearings, notices, and legal terms "
        "in simple, neutral language for public awareness."
    )

    st.markdown("## It Can Help With")
    st.write(
        "- Court case filing process\n"
        "- Hearing stages\n"
        "- Court notices and summons\n"
        "- Judicial workflow\n"
        "- Common legal terms"
    )

    st.markdown("## It Cannot Help With")
    st.write(
        "- Legal advice\n"
        "- Case outcomes\n"
        "- Legal strategy\n"
        "- Drafting legal documents"
    )

    st.markdown("## Example Questions")
    st.write(
        "- What is a court summons?\n"
        "- What happens during a hearing?\n"
        "- Explain stages of a court case"
    )

# ---------------- INPUT ----------------
st.markdown("### Ask a Question")

user_query = st.text_input(
    "Enter your question related to court procedures:",
    placeholder="e.g., What happens during a court hearing?"
)

uploaded_file = st.file_uploader(
    "Upload a court-related document (optional)",
    type=["pdf", "txt", "png", "jpg", "jpeg"]
)

# ---------------- GEMINI FUNCTION ----------------
def generate_response(user_text):
    system_prompt = """
You are a Judicial Procedure Information Assistant.
Rules:
- Explain only general court procedures and workflows
- Use simple, neutral language
- Do NOT give legal advice or case-specific opinions
- Do NOT predict outcomes
- If asked for advice, politely refuse and explain limitations
"""

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(
                text=system_prompt + "\n\nUser Question:\n" + user_text
            )],
        )
    ]

    tools = [types.Tool(googleSearch=types.GoogleSearch())]

    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
        tools=tools,
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=contents,
        config=config,
    ):
        if chunk.text:
            response_text += chunk.text

    return response_text


# ---------------- SUBMIT ----------------
if st.button("Submit"):
    if not user_query and not uploaded_file:
        st.warning("Please enter a question or upload a document.")
    else:
        with st.spinner("Processing..."):
            st.markdown("#### Response")

            query_text = user_query

            if uploaded_file:
                file_content = uploaded_file.read()
                query_text += (
                    "\n\n[User has uploaded a document for contextual understanding. "
                    "Explain only general procedural aspects.]"
                )

            response = generate_response(query_text)
            st.write(response)

# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "Disclaimer: This system is for educational and informational purposes only "
    "and does not provide legal advice."
)
