import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

app = Flask(__name__, static_folder='.')

# Initialize OpenAI Client (Reads standard OPENAI_API_KEY environment variable)
client = OpenAI()

# Simple scraper helper to grab context from a targeted URL
def fetch_forum_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            # Extract plain text content from the forum page
            return soup.get_text(separator=' ', strip=True)[:4000] # Limit to avoid context blast
    except Exception as e:
        print(f"Scraping error: {e}")
    return ""

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json or {}
    user_question = data.get('question', '')
    
    if not user_question:
        return jsonify({'answer': 'Please ask a valid question.'})
        
    # Example mapping targets based on query detection to guide your bot
    target_url = "https://forum.liverussia.online/"
    if "1.09" in user_question or "rule" in user_question.lower():
        # Point to the actual rules thread sub-URL if known
        target_url = "https://forum.liverussia.online/" 
    elif "church" in user_question.lower() or "gps" in user_question.lower():
        # Point to the vatican/support sections sub-URL if known
        target_url = "https://forum.liverussia.online/"

    # Fetch live layout context from the page
    live_context = fetch_forum_page(target_url)

    system_prompt = (
        "You are an expert AI assistant dedicated to the LIVE RUSSIA gaming forum (https://forum.liverussia.online/).\n"
        "Your task is to analyze user queries regarding server rules (like rule 1.09), faction dynamics, "
        "and in-game map coordinates (like Church GPS data from support guides).\n"
        f"Live Forum Context Sample: {live_context}\n\n"
        "Provide quick, highly accurate, and direct answers using the context provided or your training on XenForo roleplay server frameworks."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Error processing AI request: {str(e)}. Make sure your OPENAI_API_KEY environment variable is set properly on your hosting site."

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
