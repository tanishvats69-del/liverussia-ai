import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
from groq import Groq

app = Flask(__name__, static_folder='.')

# Initialize the FREE Groq client
# It automatically reads the GROQ_API_KEY environment variable
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def scrape_forum():
    try:
        url = "https://liverussia.online"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract clean visible text from the forum page
            return soup.get_text()[:4000]  # Kept within free context limits
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
        # Using Meta's powerful Llama 3 model completely for free
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful AI assistant for the LIVE RUSSIA mobile game forum. Answer the user's questions based on this live forum data: {forum_context}"
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
        return jsonify({'error': f"Error processing AI request: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
