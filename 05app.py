import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import os
import math

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="MarketLens AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Main page width */
.block-container {
    max-width: 1200px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Main title */
.main-title {
    font-size: 3rem;
    font-weight: 750;
    letter-spacing: -1.5px;
    margin-bottom: 0.3rem;
}

/* Subtitle */
.subtitle {
    font-size: 1.15rem;
    color: #9ca3af;
    margin-bottom: 2rem;
}

/* Small section label */
.section-label {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: #8b949e;
    margin-top: 1rem;
    margin-bottom: 0.4rem;
}

/* Analysis result container */
.analysis-card {
    border: 1px solid rgba(128, 128, 128, 0.25);
    border-radius: 12px;
    padding: 1.5rem 1.7rem;
    margin-top: 1rem;
    background: rgba(128, 128, 128, 0.04);
}

/* Make buttons cleaner */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    padding: 0.55rem 1.25rem;
}

/* Input styling */
.stTextInput input {
    border-radius: 8px;
}

.stTextArea textarea {
    border-radius: 8px;
}

/* Metrics */
[data-testid="stMetric"] {
    border: 1px solid rgba(128, 128, 128, 0.22);
    padding: 1rem;
    border-radius: 10px;
    background: rgba(128, 128, 128, 0.03);
}

/* Sidebar spacing */
section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* Footer */
.footer {
    text-align: center;
    color: #777;
    font-size: 0.82rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(128, 128, 128, 0.2);
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def extract_article(url):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary webpage elements
    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "aside"
    ]):
        element.decompose()

    paragraphs = soup.find_all("p")

    article_text = "\n".join(
        p.get_text(" ", strip=True)
        for p in paragraphs
        if len(p.get_text(strip=True)) > 30
    )

    return article_text


def analyze_article(article_text):

    prompt = f"""
You are a financial news analysis assistant.

Analyze the following financial news article.

Your goal is to explain the article clearly and objectively.
Do not provide personalized investment advice.

Return the analysis using EXACTLY these headings:

SUMMARY

Provide a concise summary of the article in 2-4 sentences.

SENTIMENT

Classify the overall financial sentiment as:
Positive, Negative, Neutral, or Mixed.

Briefly explain why.

AFFECTED COMPANIES & INDUSTRIES

Identify the major companies, industries, or sectors that may
be affected by the news.

POTENTIAL MARKET IMPACT

Explain how the developments described in the article could
potentially affect financial markets, businesses, or investors.

KEY RISKS

Identify the most important risks or uncertainties discussed
or implied by the article.

3 KEY TAKEAWAYS

Provide exactly three concise takeaways.

ARTICLE:

{article_text}
"""

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="openai/gpt-oss-120b",
    )

    return response.choices[0].message.content


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## MarketLens AI")

    st.caption("AI-Powered Financial News Analysis")

    st.divider()

    st.markdown("### Analysis Features")

    st.write("Article Summarization")
    st.write("Market Sentiment")
    st.write("Industry Identification")
    st.write("Risk Analysis")
    st.write("Market Impact Assessment")

    st.divider()

    st.markdown("### How It Works")

    st.caption(
        "1. Enter an article URL or paste article text.\n\n"
        "2. MarketLens extracts and processes the content.\n\n"
        "3. Generative AI produces structured market insights."
    )

    st.divider()

    st.caption("Powered by Groq")
    st.caption("Model: GPT-OSS 120B")


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="section-label">Financial Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">MarketLens AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Turn financial news into structured market intelligence
    using generative AI.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# INPUT
# --------------------------------------------------

st.markdown("### Analyze Financial News")

st.write(
    "Paste a public financial news URL or enter article text "
    "manually to generate an AI-powered market analysis."
)

input_method = st.radio(
    "Choose an input method:",
    ["Article URL", "Article Text"],
    horizontal=True
)

article_text = ""

if input_method == "Article URL":

    article_url = st.text_input(
        "Article URL",
        placeholder="https://finance.yahoo.com/..."
    )

else:

    article_text = st.text_area(
        "Article Text",
        placeholder="Paste the financial news article here...",
        height=220
    )


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

analyze = st.button(
    "Analyze Article",
    type="primary",
    use_container_width=False
)


# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

if analyze:

    try:

        # URL MODE
        if input_method == "Article URL":

            if not article_url:
                st.warning("Please enter an article URL.")
                st.stop()

            with st.spinner("Retrieving article..."):

                article_text = extract_article(article_url)

            if not article_text:
                st.error(
                    "The article text could not be extracted. "
                    "Try pasting the article text manually."
                )
                st.stop()

            st.success("Article successfully retrieved.")

        # TEXT MODE
        else:

            if not article_text.strip():
                st.warning("Please paste an article.")
                st.stop()

        # ------------------------------------------
        # ARTICLE STATISTICS
        # ------------------------------------------

        word_count = len(article_text.split())
        character_count = len(article_text)
        reading_time = max(1, math.ceil(word_count / 200))

        st.markdown("### Article Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Word Count",
                value=f"{word_count:,}"
            )

        with col2:
            st.metric(
                label="Characters",
                value=f"{character_count:,}"
            )

        with col3:
            st.metric(
                label="Estimated Reading Time",
                value=f"{reading_time} min"
            )

        # ------------------------------------------
        # AI ANALYSIS
        # ------------------------------------------

        st.markdown("### AI Market Analysis")

        with st.spinner(
            "Analyzing financial news and generating insights..."
        ):

            analysis = analyze_article(article_text)

        st.markdown(
            '<div class="analysis-card">',
            unsafe_allow_html=True
        )

        st.markdown(analysis)

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        # ------------------------------------------
        # SOURCE TEXT
        # ------------------------------------------

        with st.expander("View Source Article Text"):

            st.text_area(
                "Extracted Article",
                article_text,
                height=300,
                disabled=True
            )

    except requests.exceptions.RequestException:

        st.error(
            "The article could not be retrieved from this website. "
            "Try using the Article Text option instead."
        )

    except Exception as e:

        st.error(f"An error occurred: {e}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        <strong>MarketLens AI</strong><br>
        Financial News Analysis<br><br>
        Built with Python, Streamlit & Groq<br>
        AI-generated analysis is for informational purposes only
        and should not be considered financial advice.
    </div>
    """,
    unsafe_allow_html=True
)