#!/usr/bin/env python3
"""
Fast AgriAssist Backend - Optimized for Speed
No PDF processing, instant responses
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
from datetime import datetime

app = Flask(__name__)

# Enable CORS for all domains
CORS(app, origins=[
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
])

# Pre-defined responses for instant answers
AGRICULTURAL_RESPONSES = {
    "rice": {
        "en": "Rice cultivation in Kerala: Plant during June-July (Kharif season). Use certified seeds, maintain proper water level (2-3 cm), apply fertilizers in 3 splits. Common varieties: Jyothi, Uma, Kanakom. Harvest in 120-140 days.",
        "ml": "കേരളത്തിൽ അരി കൃഷി: ജൂൺ-ജൂലൈ മാസങ്ങളിൽ നടുക. സർട്ടിഫൈഡ് വിത്തുകൾ ഉപയോഗിക്കുക, ശരിയായ ജലനിരപ്പ് (2-3 സെ.മീ) നിലനിർത്തുക, വളം 3 ഭാഗങ്ങളായി ചെലുത്തുക."
    },
    "coconut": {
        "en": "Coconut care: Plant 8x8m spacing, water regularly, apply organic manure. Common pests: Rhinoceros beetle, red palm weevil. Use neem oil for pest control. Harvest when nuts are 12 months old.",
        "ml": "തെങ്ങ് പരിപാലനം: 8x8m ഇടവേളയിൽ നടുക, പതിവായി വെള്ളം ചെലുത്തുക, ജൈവ വളം ചെലുത്തുക. പ്രധാന കീടങ്ങൾ: കൊമ്പൻ വണ്ട്, ചുവന്ന കീടം."
    },
    "vegetables": {
        "en": "Vegetable farming tips: Use raised beds, proper spacing, regular watering. Common crops: Tomato, Brinjal, Okra, Green chili. Apply organic compost, use drip irrigation for water efficiency.",
        "ml": "പച്ചക്കറി കൃഷി നുറുങ്ങുകൾ: ഉയർന്ന കട്ടികൾ ഉപയോഗിക്കുക, ശരിയായ ഇടവേള, പതിവായി വെള്ളം. പ്രധാന വിളകൾ: തക്കാളി, വഴുതന, വെണ്ട, പച്ചമുളക്."
    },
    "pest": {
        "en": "Pest control: Use integrated pest management (IPM). Apply neem oil, use yellow sticky traps, encourage natural predators. Avoid excessive pesticide use. Monitor crops regularly.",
        "ml": "കീടനിയന്ത്രണം: സമഗ്ര കീടനിയന്ത്രണം (IPM) ഉപയോഗിക്കുക. വേപ്പെണ്ണ ചെലുത്തുക, മഞ്ഞ കുടുക്കുകൾ ഉപയോഗിക്കുക, പ്രകൃതി ശത്രുക്കളെ പ്രോത്സാഹിപ്പിക്കുക."
    },
    "weather": {
        "en": "Weather-based farming: Check weather forecast before planting. Monsoon (June-September) is best for rice. Summer (March-May) for vegetables. Use weather apps for daily updates.",
        "ml": "കാലാവസ്ഥ അടിസ്ഥാന കൃഷി: നടുന്നതിന് മുമ്പ് കാലാവസ്ഥ പ്രവചനം പരിശോധിക്കുക. മഴക്കാലം (ജൂൺ-സെപ്റ്റംബർ) അരിക്ക് ഏറ്റവും നല്ലത്."
    }
}

def get_fast_response(query, language="en"):
    """Get instant response based on query keywords"""
    query_lower = query.lower()
    
    # Check for keywords and return relevant response
    if any(word in query_lower for word in ["rice", "arisi", "nellu", "അരി", "നെല്ല്"]):
        return AGRICULTURAL_RESPONSES["rice"].get(language, AGRICULTURAL_RESPONSES["rice"]["en"])
    
    elif any(word in query_lower for word in ["coconut", "thenga", "തെങ്ങ്", "coconut"]):
        return AGRICULTURAL_RESPONSES["coconut"].get(language, AGRICULTURAL_RESPONSES["coconut"]["en"])
    
    elif any(word in query_lower for word in ["vegetable", "pachakari", "പച്ചക്കറി", "veggie"]):
        return AGRICULTURAL_RESPONSES["vegetables"].get(language, AGRICULTURAL_RESPONSES["vegetables"]["en"])
    
    elif any(word in query_lower for word in ["pest", "kida", "കീടം", "disease", "roga", "രോഗം"]):
        return AGRICULTURAL_RESPONSES["pest"].get(language, AGRICULTURAL_RESPONSES["pest"]["en"])
    
    elif any(word in query_lower for word in ["weather", "kalaavastha", "കാലാവസ്ഥ", "rain", "mazha", "മഴ"]):
        return AGRICULTURAL_RESPONSES["weather"].get(language, AGRICULTURAL_RESPONSES["weather"]["en"])
    
    else:
        # Default response
        if language == "ml":
            return f"നിങ്ങളുടെ ചോദ്യത്തിന് ഉത്തരം: {query}. കൃഷി സംബന്ധിച്ച കൂടുതൽ വിവരങ്ങൾക്ക് ഞങ്ങളുടെ വിദഗ്ധരുമായി ബന്ധപ്പെടുക. കൃഷി ആശയവിനിമയ കേന്ദ്രം: 0471-2301861"
        else:
            return f"Thank you for your question: {query}. For more agricultural information, contact our experts. Krishi Call Center: 0471-2301861. This is a fast response from AgriAssist!"

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "Fast Backend is running",
        "version": "1.0.0-fast",
        "timestamp": datetime.now().isoformat(),
        "features": ["Instant Responses", "No PDF Processing", "Optimized for Speed"]
    })

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Fast question answering endpoint"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        language = data.get('language', 'en')
        context = data.get('context', {})
        
        if not query:
            return jsonify({
                "answer": "Please provide a question.",
                "confidence": 0.0,
                "language": language,
                "responseTime": 0.001,
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Get instant response
        start_time = time.time()
        answer = get_fast_response(query, language)
        response_time = round(time.time() - start_time, 3)
        
        return jsonify({
            "answer": answer,
            "confidence": 0.95,
            "language": language,
            "responseTime": response_time,
            "timestamp": datetime.now().isoformat(),
            "sources": ["Fast Agricultural Knowledge Base"],
            "type": "instant_response"
        })
        
    except Exception as e:
        return jsonify({
            "answer": f"Error processing request: {str(e)}",
            "confidence": 0.0,
            "language": "en",
            "responseTime": 0.001,
            "timestamp": datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    print("🚀 Starting FAST AgriAssist Backend Server...")
    print("⚡ Optimized for instant responses")
    print("🌐 Server starting on http://127.0.0.1:8888")
    print("📱 Frontend can now connect to this backend")
    print("⚡ No PDF processing - instant responses!")
    
    app.run(debug=True, port=8888, host='0.0.0.0')
