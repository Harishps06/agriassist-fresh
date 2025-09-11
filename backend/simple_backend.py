#!/usr/bin/env python3
"""
Simple AgriAssist Backend - Quick Start Version
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["*"])  # Allow all origins for testing

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'Backend is running',
        'version': '1.0.0-simple',
        'message': 'Quick start backend working!'
    })

@app.route('/api/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        query = data.get('query', '')
        language = data.get('language', 'en')
        
        # Simple response for testing
        response = {
            'answer': f'I received your question: "{query}" in {language}. This is a quick test response!',
            'language': language,
            'confidence': 0.9,
            'responseTime': 0.1,
            'sources': ['Simple Backend'],
            'timestamp': '2025-09-10T22:30:00'
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Simple AgriAssist Backend...")
    print("🌐 Server starting on http://127.0.0.1:3000")
    app.run(debug=True, port=8888, host='0.0.0.0')
