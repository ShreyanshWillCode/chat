import os
import openai
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

load_dotenv()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = os.getenv("OPENAI_BASE_URL")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_message = request.args.get("msg")
    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": user_message}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("Error code:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
