from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get API key and base URL from environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

print("KEY FOUND:", "Yes" if OPENROUTER_API_KEY else "No")  # Debug to check key presence

@app.route("/")
def home():
    return render_template("index.html")  # Make sure you have this HTML file

@app.route("/get")
def chatbot_response():
    user_msg = request.args.get("msg")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": user_msg}
        ]
    }

    response = requests.post(f"{OPENAI_BASE_URL}/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        print(f"Error code: {response.status_code} - {response.text}")
        return "Sorry, something went wrong."

if __name__ == "__main__":
    app.run(debug=True)
