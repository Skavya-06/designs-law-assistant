
import streamlit as st
from main import answer_question

st.set_page_config(
    page_title="Designs Law Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --cream: #faf7f2;
    --paper: #fffdf9;
    --brown: #9a604d;
    --brown-dark: #754535;
    --ink: #292521;
    --muted: #766d65;
    --border: #e9e0d7;
}

.stApp {
    background: var(--cream);
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1180px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
    background: #f2e9e1;
    border-right: 1px solid var(--border);
}

.brand {
    text-align: center;
    padding: 1.3rem 0 1.8rem;
    border-bottom: 1px solid #dfd1c5;
    margin-bottom: 1.5rem;
}

.brand-icon {
    font-size: 2.5rem;
    color: var(--brown);
}

.brand h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    line-height: 1.2;
    color: var(--ink);
    margin: .5rem 0;
}

.brand p {
    color: var(--muted);
    font-size: .78rem;
    letter-spacing: .08em;
    line-height: 1.7;
}

.hero-label {
    color: var(--brown);
    text-transform: uppercase;
    letter-spacing: .14em;
    font-size: .78rem;
    font-weight: 700;
    margin-bottom: .6rem;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.2rem, 4vw, 3.5rem);
    line-height: 1.15;
    color: var(--ink);
    margin: 0 0 1rem;
}

.hero-copy {
    font-size: 1.08rem;
    line-height: 1.8;
    color: var(--muted);
    max-width: 760px;
    margin-bottom: 2rem;
}

.search-card {
    background: var(--paper);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.5rem 1.6rem 1.1rem;
    box-shadow: 0 8px 28px rgba(65, 43, 28, .045);
    margin: 1.5rem 0;
}

.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.65rem;
    color: var(--ink);
    margin: 1.8rem 0 .8rem;
}

.feature-card {
    background: rgba(255,253,249,.7);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem;
    min-height: 120px;
}

.feature-icon {
    font-size: 1.35rem;
    margin-bottom: .45rem;
}

.feature-title {
    font-weight: 700;
    color: var(--brown-dark);
    margin-bottom: .35rem;
}

.feature-copy {
    font-size: .88rem;
    line-height: 1.55;
    color: var(--muted);
}

.stTextArea textarea {
    background: #fffefa;
    border: 1px solid #ded4ca;
    border-radius: 12px;
    color: var(--ink);
    font-size: 1rem;
    padding: 1rem;
}

.stTextArea textarea:focus {
    border-color: var(--brown);
    box-shadow: 0 0 0 1px var(--brown);
}

.stButton > button[kind="primary"] {
    background: var(--brown);
    border: 1px solid var(--brown);
    color: white;
    border-radius: 10px;
    min-height: 3rem;
    padding: 0 1.5rem;
    font-weight: 600;
}

.stButton > button[kind="primary"]:hover {
    background: var(--brown-dark);
    border-color: var(--brown-dark);
}

.stButton > button:not([kind="primary"]) {
    border: 1px solid var(--border);
    background: var(--paper);
    color: var(--ink);
    border-radius: 11px;
    min-height: 3.3rem;
    text-align: left;
    white-space: normal;
}

.stButton > button:not([kind="primary"]):hover {
    border-color: var(--brown);
    color: var(--brown-dark);
}

.answer-card {
    background: var(--paper);
    border: 1px solid var(--border);
    border-left: 4px solid var(--brown);
    border-radius: 12px;
    padding: 1.3rem 1.5rem;
    line-height: 1.8;
    margin: .7rem 0 1rem;
}

.reference-card {
    background: #f2e9e1;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    line-height: 1.7;
    color: var(--brown-dark);
}

.footer {
    border-top: 1px solid var(--border);
    margin-top: 3rem;
    padding-top: 1.2rem;
    color: var(--muted);
    font-size: .82rem;
    text-align: center;
}

#MainMenu, footer {
    visibility: hidden;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1.5rem 1rem 3rem;
    }
    .hero-title {
        font-size: 2.2rem;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------- Example questions ----------
examples = [
    "How long does a proprietor have copyright in a registered design, and can it be extended?",
    "Which classification system is used to register designs?",
    "What is the government fee to register a trademark?",
    "Who is the current Controller General of Patents?",
    "What is the fee to register a design?",
]


def choose_question(question):
    st.session_state.question = question


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">⚖</div>
        <h2>Designs Law<br>Assistant</h2>
        <p>MANUAL OF DESIGNS PRACTICE &amp;<br>PROCEDURE · CGPDTM</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Navigate")
    st.button(
        "✦  Ask a Question",
        use_container_width=True,
        type="primary",
        key="nav_ask",
    )

    if st.button("▤  About the Project", use_container_width=True):
        st.session_state.show_about = not st.session_state.get(
            "show_about", False
        )

    if st.button("⌘  How It Works", use_container_width=True):
        st.session_state.show_how = not st.session_state.get(
            "show_how", False
        )

    st.markdown("---")
    st.caption("Built with Python · LangChain · ChromaDB · Gemini")
    st.markdown(
        "<div style='color:#766d65; font-style:italic; "
        "line-height:1.7; margin-top:2rem;'>"
        "Your guide to design law information.</div>",
        unsafe_allow_html=True,
    )


# ---------- Main page ----------
st.markdown(
    '<div class="hero-label">Your legal research companion</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-title">Welcome to Designs Law Assistant</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-copy">Ask questions about the Manual of Designs '
    'Practice &amp; Procedure, Office of the CGPDTM. '
    'Explore answers with supporting references and PDF excerpts.</div>',
    unsafe_allow_html=True,
)

if st.session_state.get("show_about", False):
    st.info(
        "This project is a document-based question-answering assistant. "
        "It retrieves relevant passages from the supplied manual and uses "
        "Gemini to formulate an answer."
    )

if st.session_state.get("show_how", False):
    st.info(
        "Your question → ChromaDB retrieves relevant PDF chunks → "
        "Gemini answers from the retrieved context → source excerpts "
        "help you verify the response."
    )

st.markdown('<div class="search-card">', unsafe_allow_html=True)
st.markdown("#### ✧  What would you like to know?")

question = st.text_area(
    "Enter your question",
    key="question",
    height=115,
    placeholder=(
        "e.g. How long does a proprietor have copyright in a "
        "registered design, and can it be extended?"
    ),
    label_visibility="collapsed",
)

left, right = st.columns([1, 2])

with left:
    ask = st.button(
        "✧  Get Answer",
        type="primary",
        use_container_width=True,
    )

with right:
    st.caption("Tip: Ask one clear, specific question for better results.")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- Results ----------
if ask:
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Searching the manual and preparing your answer..."):
            try:
                result = answer_question(question.strip())

                st.markdown(
                    '<div class="section-heading">Your Answer</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="answer-card">'
                    f'{result["answer"]}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    '<div class="section-heading">Source Reference</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="reference-card">'
                    f'<b>Reference</b><br>{result["reference"]}</div>',
                    unsafe_allow_html=True,
                )

                sources = result.get("sources", [])

                if sources:
                    st.markdown(
                        '<div class="section-heading">Verify in the Manual</div>',
                        unsafe_allow_html=True,
                    )
                    st.caption(
                        "Expand a source to inspect the retrieved PDF excerpt."
                    )

                    for source in sources:
                        with st.expander(
                            f'📄  PDF page {source.get("page", "Unknown")}'
                        ):
                            st.write(source.get("excerpt", ""))

                if result.get("answer", "").strip().lower() == "not found":
                    st.caption(
                        "The supplied document did not provide a supported answer."
                    )

            except Exception as error:
                st.error(f"Unable to generate an answer: {error}")


# ---------- Example questions ----------
st.markdown(
    '<div class="section-heading">Need a place to start?</div>',
    unsafe_allow_html=True,
)
st.write("Choose one of the questions from your assignment.")

for start in range(0, len(examples), 2):
    cols = st.columns(2)

    for offset, col in enumerate(cols):
        index = start + offset
        if index < len(examples):
            with col:
                st.button(
                    examples[index],
                    key=f"example_{index}",
                    use_container_width=True,
                    on_click=choose_question,
                    args=(examples[index],),
                )

# ---------- Feature cards ----------
st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
feature_cols = st.columns(4)

features = [
    ("📚", "Document-based", "Uses your supplied manual"),
    ("✧", "AI-assisted", "Gemini-powered answers"),
    ("🔎", "Source references", "Inspect PDF pages and excerpts"),
    ("✓", "Easy to use", "Simple question-and-answer workflow"),
]

for col, (icon, title, description) in zip(feature_cols, features):
    with col:
        st.markdown(
            f'<div class="feature-card">'
            f'<div class="feature-icon">{icon}</div>'
            f'<div class="feature-title">{title}</div>'
            f'<div class="feature-copy">{description}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown(
    '<div class="footer">Designs Law Assistant · '
    'For educational and document research purposes</div>',
    unsafe_allow_html=True,
)
