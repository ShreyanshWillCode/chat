import os
import requests
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

load_dotenv()

# Using OpenRouter API directly
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/direct")
def direct_api():
    """Route that serves a page making direct API calls to OpenRouter"""
    return render_template("direct.html")

@app.route("/get")
def get_bot_response():
    user_message = request.args.get("msg")
    try:
        # Following official OpenRouter documentation
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000"  # Required for attribution
        }
        
        payload = {
            "model": "anthropic/claude-3-haiku",  # Using Claude instead of Mistral
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
        
        print("Sending request to OpenRouter...")
        print(f"Headers: {json.dumps(headers, indent=2)}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Using json.dumps() instead of json parameter as per their examples
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            data=json.dumps(payload)
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code != 200:
            error_text = response.text
            print(f"Error: {error_text}")
            return f"API Error: {response.status_code}. Response: {error_text[:100]}", 500
        
        result = response.json()
        print(f"Success! Response: {json.dumps(result)[:100]}...")
        
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Exception: {str(e)}")
        return str(e), 500

if __name__ == "__main__":
    print(f"Starting Flask app with API key: {OPENROUTER_API_KEY[:10]}...")
    print("Access the direct API interface at: http://localhost:5000/direct")
    app.run(debug=True)
