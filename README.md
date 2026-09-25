# AI-Finacial-News-Analyzer
# AI Financial News Analyzer

AI Financial News Analyzer is a Python web application I built to make financial news easier to understand. The idea behind the project was to take long or complicated financial articles and use AI to break them down into useful information without having to read through the entire article.

The application allows users to enter a financial news article URL and receive an AI-generated analysis of the article.

## Features

- Summarizes financial news articles
- Identifies the main points and takeaways from an article
- Provides insights into the potential market impact of the news
- Allows users to analyze articles directly from a URL
- Includes access to recent financial news
- Uses a simple Streamlit interface to make the application easy to use

## Technologies Used

- **Python** – Main programming language
- **Streamlit** – Used to build the web interface
- **Groq API** – Used to generate AI-powered summaries and analysis
- **Article extraction tools** – Used to retrieve article content from URLs

## How It Works

1. The user enters the URL of a financial news article.
2. The application extracts the text from the article.
3. The article content is sent to the Groq API.
4. The AI analyzes the article and returns a more organized summary with important information and market insights.
5. The results are displayed through the Streamlit interface.

## Why I Built This

I built this project because I wanted to get more hands-on experience working with AI and APIs while also creating something related to my interest in financial markets.

Financial news can sometimes be long and difficult to quickly understand, especially when several articles are covering different companies or events. I wanted to create a tool that could make it easier to pull out the most important information from an article.

This project also gave me experience working with generative AI, API integration, web applications, and processing information from external sources.

## Running the Project

First, clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd YOUR_REPOSITORY_NAME
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Add your Groq API key. Do not upload your actual API key to GitHub.

Then run the Streamlit application:

```bash
streamlit run app.py
```

## Future Improvements

Some features I would like to add in the future include better article extraction, analysis of multiple articles at once, company-specific news tracking, and more detailed market sentiment analysis.

