import streamlit as st


st.set_page_config(
    page_title="AI Doc Agent",
    page_icon="📄",
    layout="wide",
)


# ---------- Custom CSS ----------

st.markdown(
    """
    <style>

    /* Main container */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .app-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        color: #777;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* Section titles */
    .section-title {
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-top: 1.5rem;
        margin-bottom: 0.6rem;
        color: #555;
    }

    /* Cards */
    .card {
        padding: 1.5rem;
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    /* Status */
    .status {
        display: inline-block;
        padding: 0.35rem 0.7rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Header ----------

st.markdown(
    '<div class="app-title">📄 AI Doc Agent</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-subtitle">'
    'Intelligent document analysis powered by RAG'
    '</div>',
    unsafe_allow_html=True,
)


# ---------- Status ----------

col1, col2 = st.columns([6, 1])

with col2:
    st.markdown(
        '<div class="status">● Ready</div>',
        unsafe_allow_html=True,
    )


# ---------- Document ----------

st.markdown(
    '<div class="section-title">DOCUMENT</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
    label_visibility="collapsed",
)


if uploaded_file:
    st.success(f"Document selected: {uploaded_file.name}")


# ---------- Question ----------

st.markdown(
    '<div class="section-title">ASK YOUR DOCUMENT</div>',
    unsafe_allow_html=True,
)

question = st.text_area(
    "Question",
    placeholder="What would you like to know about this document?",
    height=120,
    label_visibility="collapsed",
)


st.button(
    "Analyze Document",
    type="primary",
    use_container_width=True,
)


# ---------- Answer ----------

st.markdown(
    '<div class="section-title">ANSWER</div>',
    unsafe_allow_html=True,
)

st.info(
    "Upload a document and ask a question to see the AI-generated answer."
)