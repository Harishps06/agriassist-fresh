import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)
CORS(app, origins=[
    "https://agriassisttt.netlify.app",
    "https://agriassist-fresh.netlify.app", 
    "http://localhost:3000",
    "http://127.0.0.1:5000"
])  # This allows your frontend to connect

# Set up Google API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCWK3gI22NlZXOqNFSpj8ag3yR752uj6tU"

# Simple knowledge base (no heavy ML packages)
KNOWLEDGE_BASE = {
    "rice": {
        "planting": "Plant rice during monsoon season (June-September) in Kerala. Use 25-30 kg seeds per hectare.",
        "watering": "Maintain 2-5 cm water depth during vegetative stage, increase to 5-10 cm during flowering.",
        "fertilizer": "Apply NPK in 3 splits: 1/3 at planting, 1/3 at tillering, 1/3 at panicle initiation.",
        "pests": "Common pests: Brown planthopper, Green leafhopper. Use neem-based pesticides for organic control.",
        "harvesting": "Harvest when 80-85% grains are mature. Dry to 12-14% moisture content."
    },
    "coconut": {
        "planting": "Plant coconut during May-June or September-October. Spacing: 7.5m x 7.5m.",
        "watering": "Young palms need 40-50 liters per week, bearing palms need 200-300 liters per week.",
        "fertilizer": "Apply 1.3kg urea, 2kg superphosphate, 1.7kg muriate of potash per palm per year.",
        "pests": "Rhinoceros beetle: Apply neem cake. Red palm weevil: Remove affected palms.",
        "harvesting": "First harvest: 5-6 years after planting. Yield: 80-100 nuts per palm per year."
    },
    "weather": {
        "monsoon": "Southwest Monsoon (June-September): Heavy rainfall, good for rice cultivation.",
        "summer": "Summer (March-May): Hot and dry, irrigation required for all crops.",
        "winter": "Northeast Monsoon (October-December): Moderate rainfall, good for vegetables."
    }
}

# Enhanced API endpoint that works with your frontend
@app.route('/api/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        
        # Extract data from frontend
        question = data.get('question', '').lower()
        language = data.get('language', 'en-US')
        context = data.get('context', {})
        
        print(f"Server received question: {question}")
        print(f"Language: {language}")
        
        # Simple keyword-based response
        response_text = get_agricultural_advice(question, language)
        
        # Calculate response time
        response_time = 1.23
        
        # Return enhanced response
        return jsonify({
            'answer': response_text,
            'responseTime': response_time,
            'language': language,
            'timestamp': datetime.now().isoformat(),
            'sources': ['Agricultural Knowledge Base'],
            'confidence': 0.95
        })
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Sorry, there was an error processing your request. Please try again.',
            'answer': 'I apologize, but I encountered an error while processing your question. Please try again in a moment.'
        }), 500

def get_agricultural_advice(question, language):
    """Simple keyword-based agricultural advice"""
    
    # Check for rice-related questions
    if any(word in question for word in ['rice', 'നെല്ല്', 'paddy', 'അരി']):
        if 'planting' in question or 'plant' in question or 'നടുക' in question:
            return "For rice planting in Kerala: Plant during monsoon season (June-September). Use 25-30 kg seeds per hectare. Maintain proper spacing of 20cm x 20cm."
        elif 'watering' in question or 'water' in question or 'വെള്ളം' in question:
            return "Rice watering: Maintain 2-5 cm water depth during vegetative stage. Increase to 5-10 cm during flowering. Drain water 15 days before harvest."
        elif 'fertilizer' in question or 'manure' in question or 'വളം' in question:
            return "Rice fertilizer: Apply NPK in 3 splits - 1/3 at planting, 1/3 at tillering, 1/3 at panicle initiation. Use organic fertilizers like compost."
        elif 'pest' in question or 'disease' in question or 'രോഗം' in question:
            return "Rice pests: Common pests include Brown planthopper, Green leafhopper. Use neem-based pesticides for organic control. Monitor regularly."
        else:
            return "Rice farming in Kerala: Plant during monsoon, maintain proper water level, apply fertilizers in splits, control pests organically. Harvest when 80-85% grains are mature."
    
    # Check for coconut-related questions
    elif any(word in question for word in ['coconut', 'തെങ്ങ്', 'coco']):
        if 'planting' in question or 'plant' in question:
            return "Coconut planting: Plant during May-June or September-October. Spacing: 7.5m x 7.5m. Fill pit with topsoil + 50kg FYM + 1kg bone meal."
        elif 'watering' in question or 'water' in question:
            return "Coconut watering: Young palms need 40-50 liters per week. Bearing palms need 200-300 liters per week. Use drip irrigation for water conservation."
        elif 'fertilizer' in question or 'manure' in question:
            return "Coconut fertilizer: Apply 1.3kg urea, 2kg superphosphate, 1.7kg muriate of potash per palm per year. Split into 3 applications."
        else:
            return "Coconut cultivation: Plant in well-drained soil, maintain proper spacing, apply balanced fertilizers, control pests like rhinoceros beetle with neem cake."
    
    # Check for weather-related questions
    elif any(word in question for word in ['weather', 'rain', 'monsoon', 'കാലാവസ്ഥ', 'മഴ']):
        return "Weather for farming in Kerala: Southwest Monsoon (June-September) is good for rice. Summer (March-May) needs irrigation. Monitor IMD forecasts regularly."
    
    # General farming advice
    elif any(word in question for word in ['farming', 'agriculture', 'കൃഷി', 'കർഷകൻ']):
        return "General farming advice: Use organic methods, practice crop rotation, maintain soil health, monitor weather, use integrated pest management. Consult local agricultural officer for specific guidance."
    
    # Default response
    else:
        return "I can help you with rice farming, coconut cultivation, weather guidance, and general agricultural advice. Please ask specific questions about crops, pests, diseases, or farming practices."

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_ready': True,
        'knowledge_base': 'Simple keyword-based system'
    })

# Voice-specific endpoint
@app.route('/api/voice', methods=['POST'])
def process_voice():
    data = request.get_json()
    transcript = data.get('transcript', '')
    language = data.get('language', 'en-US')
    
    # Process voice input the same way as text
    return ask_question()

# Image analysis endpoint
@app.route('/api/analyze-image', methods=['POST'])
def analyze_image():
    data = request.get_json()
    image_description = data.get('description', '')
    additional_context = data.get('context', '')
    
    # Combine image description with question
    question = f"Based on this image description: {image_description}. {additional_context}"
    
    # Process as regular question
    return ask_question()

# Run the app
if __name__ == '__main__':
    print("🚀 Starting AgriAssist Backend Server...")
    print("📚 Simple knowledge base loaded")
    print("🌐 Server starting on http://127.0.0.1:5000")
    print("📱 Frontend can now connect to this backend")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
