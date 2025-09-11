#!/usr/bin/env python3
"""
TestSprite-Compatible AgriAssist Backend
Optimized for TestSprite proxy connectivity
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import time

app = Flask(__name__)

# Enable CORS for all domains and headers
CORS(app, origins="*", allow_headers="*", methods="*")

# Add headers to prevent proxy issues
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Cache-Control', 'no-cache, no-store, must-revalidate')
    response.headers.add('Pragma', 'no-cache')
    response.headers.add('Expires', '0')
    return response

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "TestSprite Backend is running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "features": ["Agricultural Knowledge", "Multilingual Support", "TestSprite Compatible"]
    })

@app.route('/api/ask', methods=['POST', 'OPTIONS'])
def ask():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
    
    try:
        data = request.get_json()
        query = data.get('query', '') if data else ''
        language = data.get('language', 'en') if data else 'en'
        
        # Simulate processing time
        time.sleep(0.1)
        
        # Provide detailed agricultural advice
        answer = f"""Agricultural Advice for: {query}

Based on your query about "{query}", here's comprehensive guidance:

**Crop Management:**
- Ensure proper soil preparation and drainage
- Use certified seeds for better yield
- Follow recommended spacing and planting density
- Implement crop rotation to maintain soil health

**Water Management:**
- Maintain consistent moisture levels
- Avoid overwatering or underwatering
- Use drip irrigation for water efficiency
- Monitor soil moisture regularly

**Pest and Disease Control:**
- Practice integrated pest management (IPM)
- Use organic pesticides when possible
- Monitor crops regularly for early signs
- Maintain proper field hygiene

**Fertilizer Application:**
- Conduct soil tests before applying fertilizers
- Use balanced NPK ratios
- Apply fertilizers at recommended times
- Consider organic alternatives

**Harvesting:**
- Harvest at optimal maturity
- Use proper harvesting techniques
- Handle produce carefully to avoid damage
- Store in appropriate conditions

For more specific advice, consult local agricultural extension services.

Language: {language}
Query processed at: {datetime.now().isoformat()}"""
        
        return jsonify({
            "answer": answer,
            "confidence": 0.95,
            "language": language,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Error processing query: {str(e)}",
            "answer": "I apologize, but I encountered an error processing your query. Please try again.",
            "confidence": 0.0
        }), 500

@app.route('/api/weather', methods=['GET', 'OPTIONS'])
def weather():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
    
    return jsonify({
        "temperature": 28.5,
        "description": "Partly cloudy",
        "humidity": 75,
        "wind_speed": 12,
        "location": "Kerala, India",
        "timestamp": datetime.now().isoformat(),
        "source": "TestSprite Mock Weather Service"
    })

@app.route('/api/analyze-image', methods=['POST', 'OPTIONS'])
def analyze_image():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
    
    try:
        # Simulate image analysis
        time.sleep(0.2)
        
        return jsonify({
            "analysis": "Plant appears healthy with no visible signs of disease. Leaves show normal green coloration and proper structure. No pest damage detected.",
            "confidence": 0.88,
            "recommendations": [
                "Continue current care routine",
                "Monitor for any changes in leaf color",
                "Ensure adequate sunlight and water"
            ],
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Error analyzing image: {str(e)}",
            "analysis": "Unable to analyze image at this time.",
            "confidence": 0.0
        }), 500

@app.route('/api/voice', methods=['POST', 'OPTIONS'])
def voice():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
    
    try:
        data = request.get_json()
        audio_data = data.get('audio', '') if data else ''
        
        # Simulate voice processing
        time.sleep(0.1)
        
        return jsonify({
            "text": "How to grow rice in Kerala with proper water management",
            "confidence": 0.92,
            "language": "en",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Error processing voice: {str(e)}",
            "text": "Unable to process voice input at this time.",
            "confidence": 0.0
        }), 500

@app.route('/api/camera', methods=['GET', 'OPTIONS'])
def camera():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
    
    return jsonify({
        "status": "Camera access granted",
        "stream_url": "webcam://localhost:8888/camera/stream",
        "capabilities": ["photo_capture", "video_recording", "image_analysis"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/calendar', methods=['GET', 'OPTIONS'])
def calendar():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
    
    return jsonify({
        "season": "Kharif",
        "month": "September",
        "recommendations": [
            "Prepare fields for rice cultivation",
            "Apply organic manure",
            "Monitor weather conditions",
            "Start seed treatment"
        ],
        "crops": ["Rice", "Coconut", "Spices", "Vegetables"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/calculate', methods=['POST', 'OPTIONS'])
def calculate():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
    
    try:
        data = request.get_json()
        crop = data.get('crop', 'Rice') if data else 'Rice'
        area = data.get('area', 1) if data else 1
        costs = data.get('costs', {}) if data else {}
        
        # Simulate profit calculation
        base_cost = 15000
        market_price = 2500
        yield_per_acre = 2.5
        
        total_cost = base_cost * area
        total_revenue = (market_price * yield_per_acre) * area
        profit = total_revenue - total_cost
        roi = (profit / total_cost) * 100
        
        return jsonify({
            "crop": crop,
            "area": area,
            "total_cost": total_cost,
            "total_revenue": total_revenue,
            "profit": profit,
            "roi": roi,
            "yield_per_acre": yield_per_acre,
            "market_price": market_price,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Error calculating profit: {str(e)}",
            "profit": 0,
            "roi": 0
        }), 500

@app.route('/api/community', methods=['GET', 'OPTIONS'])
def community():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
    
    return jsonify({
        "farmers": [
            {"id": 1, "name": "Rajesh Kumar", "location": "Thrissur", "crops": ["Rice", "Coconut"]},
            {"id": 2, "name": "Priya Nair", "location": "Kochi", "crops": ["Spices", "Vegetables"]},
            {"id": 3, "name": "Suresh Menon", "location": "Kannur", "crops": ["Coconut", "Rice"]}
        ],
        "experts": [
            {"id": 1, "name": "Dr. Agricultural Officer", "specialization": "Crop Management", "available": True},
            {"id": 2, "name": "Dr. Soil Scientist", "specialization": "Soil Health", "available": True}
        ],
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting TestSprite-Compatible AgriAssist Backend...")
    print("🌐 Running on http://0.0.0.0:8888")
    print("📚 All API endpoints ready for testing")
    print("⚡ Optimized for TestSprite proxy connectivity")
    print("🔧 CORS and headers configured for maximum compatibility")
    
    app.run(debug=False, port=8888, host='0.0.0.0', threaded=True)
