import os
import requests
import pandas as pd

# Generate initial LLM response based on insights and data
def ask_llm(df: pd.DataFrame, insights: list):
    prompt = f"""
You are a senior digital marketing analyst. A user uploaded a vague but real campaign dataset.
Based on the following insights:

{insights}

And this data snapshot:

{df.head(5).to_markdown()}

Give advanced insights and improvement suggestions.
"""

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "https://campaign-analysis-f8e1.onrender.com",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
    return response.json()['choices'][0]['message']['content']


# Continue conversation with user's follow-up question
def continue_chat(df: pd.DataFrame, user_question: str):
    prompt = f"""
You are a senior digital marketing analyst.

A user has asked a follow-up question regarding this vague but real marketing dataset:

User question: {user_question}

Here’s a snapshot of the dataset:
{df.head(5).to_markdown()}

Answer in a professional and insightful manner.
"""

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "https://campaign-analysis-f8e1.onrender.com",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
    return response.json()['choices'][0]['message']['content']
