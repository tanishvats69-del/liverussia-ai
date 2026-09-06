import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
from groq import Groq

app = Flask(__name__, static_folder='.')

# Connect to Groq using the FREE key environment variable
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def scrape_forum():
    try:
        url = "https://liverussia.online"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text()[:4000]
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
        return jsonify({'error': 'No question provided'}), 400
        
    forum_context = scrape_forum()
    
    try:
        # Correctly structured Groq free pipeline request
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
    
        messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful AI assistant for the LIVE RUSSIA mobile game forum. Answer the user's questions clearly in English based on this forum text: {forum_context}. If asked about rules like 1.09 or location coordinates (GPS), explain them clearly using this data framework."
                },
                {
                    "role": "user",
                    "content": user_question
                }
            ]
        )
        # VERIFIED CORRECT SYNTAX: Grab the exact text string from choices
        ai_response = completion.choices[0].message.content
        return jsonify({'response': ai_response})
        
    except Exception as e:
        # This catches any credential issues cleanly so your UI doesn't display empty blocks
        return jsonify({'response': f"AI processing error: Please double check that your GROQ_API_KEY is pasted perfectly into your Render settings! (Details: {str(e)})"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

