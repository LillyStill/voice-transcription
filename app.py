# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

LEMONFOX_API_KEY = os.getenv('LEMONFOX_API_KEY')

if not LEMONFOX_API_KEY:
    raise ValueError("No LemonFox API key found. Make sure to add it to your .env file!")

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    audio_file = request.files['file']
    
    url = "https://api.lemonfox.ai/v1/audio/transcriptions"
    
    headers = {
        "Authorization": f"Bearer {LEMONFOX_API_KEY}"
    }
    
    try:
        files = {
            'file': (audio_file.filename, audio_file.stream, audio_file.content_type)
        }
        
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()
        return jsonify(response.json())
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat_completion():
    try:
        data = request.json
        
        url = "https://api.lemonfox.ai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {LEMONFOX_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Forward the request to LemonFox API
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        return jsonify(response.json())
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)