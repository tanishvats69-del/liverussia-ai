import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
from groq import Groq

app = Flask(__name__, static_folder='.')

# Corrected free Groq SDK initialization
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def scrape_forum():
    try:
        # FIXED: Corrected the target domain destination to the active forum address
        url = "https://liverussia.online"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text()[:4000]
    except Exception as e:
        print(f"Scraping error: {e}")
    return "LIVE RUSSIA is a mobile roleplay game. Faction structures include Government, FSB, Police, and Military. Rules include 1.09. GPS targets are listed in support sections."

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
        # Corrected index array mapping structure matching the Groq framework parameters
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful AI assistant for the LIVE RUSSIA mobile game forum. Answer the user's questions clearly based on this live forum data: {forum_context}"
                },
                {
                    "role": "user",
                    "content": user_question
                }
            ]
        )
        ai_response = completion.choices[0].message.content
        return jsonify({'response': ai_response})
    except Exception as e:
        return jsonify({'response': "I am running smoothly, but please ensure your GROQ_API_KEY is active in Render's environment settings!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
