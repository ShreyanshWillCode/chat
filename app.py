from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # .env file load kar dega

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")

if not API_KEY or not BASE_URL:
    raise Exception("API Key or Base URL not set in environment variables!")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.route('/')
def home():
    return render_template('index.html')  # Make sure you have index.html in templates/

@app.route('/get')
def chatbot_response():
    user_msg = request.args.get('msg')
    if not user_msg:
        return jsonify({"error": "No message sent"}), 400

    data = {
        "model": "openai/chatgpt-4",
        "messages": [{"role": "user", "content": user_msg}],
        "max_tokens": 100,
        "temperature": 0.7,
    }

    response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        res_json = response.json()
        # Adjust this according to the API response structure
        answer = res_json['choices'][0]['message']['content']
        return jsonify({"response": answer})
    else:
        return jsonify({"error": f"API request failed with status {response.status_code}", "details": response.text}), 500


if __name__ == '__main__':
    app.run(debug=True)
