
import streamlit as st
import requests

# ============================================================
# CONFIG
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Doc Agent",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# SESSION STATE
# ============================================================

if "answer" not in st.session_state:
    st.session_state.answer = None

if "sources" not in st.session_state:
    st.session_state.sources = []

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "document_processed" not in st.session_state:
    st.session_state.document_processed = False


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .block-container {
        max-width: 1050px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    /* ========================================================
       HEADER
       ======================================================== */

    .app-title {
        font-size: 2.35rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        color: #777;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    /* ========================================================
       STATUS
       ======================================================== */

    .status-container {
        display: flex;
        justify-content: flex-end;
        padding-top: 0.4rem;
    }

    .status {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
    }

    .status-online {
        color: #24733b;
        background: rgba(36, 115, 59, 0.08);
        border: 1px solid rgba(36, 115, 59, 0.18);
    }

    .status-offline {
        color: #a33;
        background: rgba(170, 50, 50, 0.08);
        border: 1px solid rgba(170, 50, 50, 0.18);
    }

    /* ========================================================
       SECTION LABEL
       ======================================================== */

    .section-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        color: #777;
        margin-top: 1.8rem;
        margin-bottom: 0.65rem;
    }

    /* ========================================================
       DOCUMENT CARD
       ======================================================== */

    .document-card {
        padding: 1rem 1.1rem;
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        margin-bottom: 0.8rem;
    }

    .document-name {
        font-size: 0.9rem;
        font-weight: 600;
    }

    .document-meta {
        color: #888;
        font-size: 0.74rem;
        margin-top: 0.25rem;
    }

    /* ========================================================
       QUESTION AREA
       ======================================================== */

    .question-help {
        color: #888;
        font-size: 0.78rem;
        margin-bottom: 0.65rem;
    }

    textarea {
        border-radius: 10px !important;
    }

    /* ========================================================
       ANSWER HEADER
       ======================================================== */

    .answer-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1.8rem;
        margin-bottom: 0.7rem;
    }

    .answer-title {
        font-size: 1rem;
        font-weight: 650;
    }

    .answer-badge {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        padding: 0.3rem 0.55rem;
        border-radius: 999px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }

    .answer-description {
        color: #888;
        font-size: 0.76rem;
        margin-bottom: 0.8rem;
    }

    /* ========================================================
       SOURCES
       ======================================================== */

    .sources-description {
        color: #888;
        font-size: 0.76rem;
        margin-bottom: 0.7rem;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 9px;
        min-height: 2.65rem;
        font-weight: 600;
    }

    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([5, 1])

with header_left:

    st.markdown(
        """
        <div class="app-title">
            📄 AI Doc Agent
        </div>

        <div class="app-subtitle">
            Ask questions and extract insights from your documents
            using retrieval-augmented generation.
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:

    try:

        health_response = requests.get(
            f"{API_URL}/health",
            timeout=3,
        )

        if health_response.status_code == 200:

            st.markdown(
                """
                <div class="status-container">
                    <div class="status status-online">
                        ● Online
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                """
                <div class="status-container">
                    <div class="status status-offline">
                        ● Offline
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    except requests.exceptions.RequestException:

        st.markdown(
            """
            <div class="status-container">
                <div class="status status-offline">
                    ● Offline
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# DOCUMENT UPLOAD
# ============================================================

st.markdown(
    '<div class="section-label">DOCUMENT</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"],
    label_visibility="collapsed",
)


if uploaded_file is not None:

    st.session_state.document_name = uploaded_file.name

    st.markdown(
        f"""
        <div class="document-card">

            <div class="document-name">
                📄 {uploaded_file.name}
            </div>

            <div class="document-meta">
                PDF document · Ready to process
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "Process Document",
        type="primary",
        use_container_width=True,
    ):

        try:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf",
                )
            }

            with st.spinner("Processing document..."):

                response = requests.post(
                    f"{API_URL}/upload",
                    files=files,
                    timeout=120,
                )

            if response.status_code == 200:

                st.session_state.document_processed = True

                st.success(
                    "Document processed successfully."
                )

            else:

                st.error(
                    f"Document processing failed "
                    f"({response.status_code})."
                )

                try:

                    error_data = response.json()

                    st.write(
                        error_data.get(
                            "detail",
                            response.text,
                        )
                    )

                except Exception:

                    st.write(response.text)

        except requests.exceptions.RequestException as e:

            st.error(
                f"Cannot connect to FastAPI: {e}"
            )


# ============================================================
# QUESTION
# ============================================================

st.markdown(
    '<div class="section-label">ASK YOUR DOCUMENT</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="question-help">
        Ask a question about the information contained in your PDF.
    </div>
    """,
    unsafe_allow_html=True,
)

question = st.text_area(
    "Question",
    placeholder=(
        "Example: What are the main conclusions of this document?"
    ),
    height=120,
    label_visibility="collapsed",
)


if st.button(
    "✨ Analyze Document",
    type="primary",
    use_container_width=True,
):

    if not question.strip():

        st.warning(
            "Please enter a question first."
        )

    else:

        try:

            with st.spinner(
                "Searching the document and generating an answer..."
            ):

                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "question": question.strip()
                    },
                    timeout=120,
                )

            if response.status_code == 200:

                data = response.json()

                st.session_state.answer = data.get(
                    "answer",
                    "",
                )

                st.session_state.sources = data.get(
                    "sources",
                    [],
                )

                st.rerun()

            else:

                st.error(
                    f"Request failed ({response.status_code})."
                )

                try:

                    error_data = response.json()

                    st.write(
                        error_data.get(
                            "detail",
                            response.text,
                        )
                    )

                except Exception:

                    st.write(response.text)

        except requests.exceptions.RequestException as e:

            st.error(
                f"Cannot connect to FastAPI: {e}"
            )


# ============================================================
# AI RESPONSE
# ============================================================

if st.session_state.answer:

    st.markdown(
        '<div class="section-label">AI RESPONSE</div>',
        unsafe_allow_html=True,
    )

    answer_left, answer_right = st.columns([4, 1])

    with answer_left:

        st.markdown(
            '<div class="answer-title">Answer</div>',
            unsafe_allow_html=True,
        )

    with answer_right:

        st.markdown(
            '<div class="answer-badge">RAG GENERATED</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="answer-description">
            Generated using information retrieved from your document.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Native Streamlit rendering.
    # No HTML div is wrapped around this component.
    st.markdown(
        st.session_state.answer
    )


# ============================================================
# SOURCES
# ============================================================

if st.session_state.sources:

    st.markdown(
        '<div class="section-label">SOURCES</div>',
        unsafe_allow_html=True,
    )

    source_count = len(
        st.session_state.sources
    )

    st.markdown(
        f"""
        <div class="sources-description">
            {source_count}
            relevant
            {"section was" if source_count == 1 else "sections were"}
            retrieved from your document.
        </div>
        """,
        unsafe_allow_html=True,
    )

    for index, source in enumerate(
        st.session_state.sources,
        start=1,
    ):

        page = source.get(
            "page",
            "Unknown",
        )

        content = source.get(
            "content",
            "",
        )

        with st.expander(
            f"Source {index}  ·  Page {page}"
        ):

            st.caption(
                f"Retrieved from page {page}"
            )

            st.write(content)

