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
        system_prompt = (
            f"You are the absolute master AI guide for the LIVE RUSSIA mobile roleplay game forum. "
            f"Answer all questions with total accuracy using this full comprehensive database: {forum_context}. "
            f"STRICT COMPLIANCE MANDATES: "
            f"1. You must write your responses entirely and completely in English only. "
            f"2. Never print out any Russian text, Cyrillic letters, or words from the source files. Always translate them seamlessly into clean English strings. "
            f"3. When answering about any terminology (IC, OOC, DM, DB, SK, RK, PG, MG), server rules (1.01 to 1.13), warn restrictions, or forum rules, output the full definition alongside its exact punishment details from the reference context. "
            f"4. If a user asks for general paths, guide them through the exact /gps sub-menu listings translated into English."
        )

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ]
        )
        
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
