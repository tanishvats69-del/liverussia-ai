import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
from groq import Groq

app = Flask(__name__, static_folder='.')

# Connect to Groq using the FREE key environment variable
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def scrape_forum():
    real_game_database = """
    LIVE RUSSIA SERVER PROJECT RULES (Официальные правила проекта):
    - Rule 1.09 (Правило 1.09): It is strictly forbidden to use, distribute, or hide any form of third-party software, cheats, scripts, hacks, cleo mods, or programs that give an unfair gameplay advantage over other players. Violating rule 1.09 results in a permanent account ban (Перманентная блокировка аккаунта) across all server networks.
    
    REAL GAME GPS COMMAND MENU PATHS (/gps):
    - GPS of Church (Церковь / Храм): /gps -> Важные места (Public Places) -> Церковь г. Арзамас (Arzamas Church / Vatican Server Section).
    - GPS of Mosque (Мечеть): /gps -> Важные места (Public Places) -> Мечеть (Mosque).
    - Government Base (Правительство): /gps -> Государственные организации (State Organizations) -> Правительство (Government).
    - FSB Base (ФСБ): /gps -> Государственные организации (State Organizations) -> Федеральная Служба Безопасности (FSB).
    - Police Station (ГИБДД / УМВД): /gps -> Государственные организации (State Organizations) -> ГИБДД (г. Южный) or УМВД (г. Арзамас).
    - Military Barracks / Army (Армия / ВЧ): /gps -> Государственные организации (State Organizations) -> Воинская часть (Army).
    
    FORUM SECTIONS & APPLICATIONS:
    - Support Agent Section (Раздел игровых помощников): Located under the main forum -> Server Section (Выбор сервера) -> Жалобы / Вопросы -> Раздел Агентов Поддержки. Players use this to view helper commands or apply for support roles.
    - Faction Leaders: Applications to run state organizations or criminal organizations (OPG) are managed via the dedicated "Заявления на пост лидера" sub-forums on each individual game server page.
    """
    try:
        url = "https://liverussia.online"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text()[:3000]
            return text_content + "\n" + real_game_database
    except Exception as e:
        print(f"Scraper backup active: {e}")
    return real_game_database

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
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are the official expert AI assistant for the LIVE RUSSIA mobile roleplay game forum. "
                        f"Your job is to answer questions with 100% factual accuracy based on this real server data: {forum_context}. "
                        f"CRITICAL RULES FOR LANGUAGE: "
                        f"1. You must reply entirely and completely in English only. "
                        f"2. Do not use Russian characters in your explanation. Always translate Russian menu paths into clear English text (for example, translate 'Важные места' to 'Public Places', and 'Церковь' to 'Church / Cathedral') so the user can easily understand them. "
                        f"3. If the user asks about Rule 1.09, explain that it strictly bans cheats and hacks, resulting in a permanent ban. "
                        f"4. If the user asks for the GPS of any building, list the path menu steps clearly in English format."
                    )
                },
                {
                    "role": "user",
                    "content": user_question
                }
            ]
        )
        
        # Safe response extraction block
        if hasattr(completion, 'choices') and len(completion.choices) > 0:
            choice = completion.choices[0]
            if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                ai_response = choice.message.content
            elif isinstance(choice, dict) and 'message' in choice:
                ai_response = choice['message'].get('content', '')
            else:
                ai_response = str(choice)
        else:
            ai_response = str(completion)
            
        return jsonify({'response': ai_response})
        
    except Exception as e:
        return jsonify({'response': f"AI Connection Error. Details: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
