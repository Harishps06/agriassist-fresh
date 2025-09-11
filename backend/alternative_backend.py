#!/usr/bin/env python3
"""
Alternative AgriAssist Backend - Fast Response Version
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["*"])  # Allow all origins

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'Alternative backend running',
        'version': '1.0.0-fast',
        'message': 'Fast response backend working!',
        'port': 7777
    })

@app.route('/api/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        query = data.get('query', '')
        language = data.get('language', 'en')
        
        # Simulate quick processing
        time.sleep(0.5)  # Just 0.5 seconds delay
        
        # Generate a quick response
        response = {
            'answer': f'I received your question: "{query}" in {language}. This is a fast response from the alternative backend! For detailed agricultural advice, please ask specific questions about crops, pests, diseases, or farming practices.',
            'language': language,
            'confidence': 0.9,
            'responseTime': 0.5,
            'sources': ['Alternative Backend - Fast Response'],
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S')
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Alternative AgriAssist Backend...")
    print("🌐 Server starting on http://127.0.0.1:3333")
    print("⚡ Fast response mode enabled")
    app.run(debug=True, port=3333, host='0.0.0.0')
