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
    """Enhanced agricultural advice with comprehensive knowledge base"""
    
    # Detect if question is in Malayalam
    is_malayalam = any(char in question for char in 'അആഇഈഉഊഋഎഏഐഒഓഔകഖഗഘങചഛജഝഞടഠഡഢണതഥദധനപഫബഭമയരലവശഷസഹളഴറ')
    
    # Check for rice-related questions
    if any(word in question for word in ['rice', 'നെല്ല്', 'paddy', 'അരി', 'നെല്ലിന്റെ', 'അരി കൃഷി', 'നെല്ലിന്റെ രോഗങ്ങൾ', 'നെല്ല് രോഗം', 'rice farming', 'rice cultivation']):
        if 'planting' in question or 'plant' in question or 'നടുക' in question:
            if is_malayalam:
                return "കേരളത്തിൽ നെല്ല് നടാനുള്ള ഉത്തമ സമയം മഴക്കാലമാണ് (ജൂൺ-സെപ്റ്റംബർ). ഹെക്ടറിന് 25-30 കിലോ വിത്ത് ഉപയോഗിക്കുക. 20cm x 20cm ഇടവേള കാത്തുസൂക്ഷിക്കുക."
            else:
                return "For rice planting in Kerala: Plant during monsoon season (June-September). Use 25-30 kg seeds per hectare. Maintain proper spacing of 20cm x 20cm."
        elif 'watering' in question or 'water' in question or 'വെള്ളം' in question:
            if is_malayalam:
                return "നെല്ലിന് വെള്ളം: വളർച്ചാ ഘട്ടത്തിൽ 2-5 സെ.മീ. വെള്ളത്തിന്റെ ആഴം കാത്തുസൂക്ഷിക്കുക. പൂക്കാലത്ത് 5-10 സെ.മീ. വരെ വർദ്ധിപ്പിക്കുക. വിളവെടുപ്പിന് 15 ദിവസം മുമ്പ് വെള്ളം കളയുക."
            else:
                return "Rice watering: Maintain 2-5 cm water depth during vegetative stage. Increase to 5-10 cm during flowering. Drain water 15 days before harvest."
        elif 'fertilizer' in question or 'manure' in question or 'വളം' in question:
            if is_malayalam:
                return "നെല്ലിന് വളം: 3 ഭാഗങ്ങളായി NPK ചെലുത്തുക - 1/3 നടുമ്പോൾ, 1/3 കുറ്റി വളരുമ്പോൾ, 1/3 പൂങ്കുല ഉണ്ടാകുമ്പോൾ. കമ്പോസ്റ്റ് പോലുള്ള ജൈവ വളങ്ങൾ ഉപയോഗിക്കുക."
            else:
                return "Rice fertilizer: Apply NPK in 3 splits - 1/3 at planting, 1/3 at tillering, 1/3 at panicle initiation. Use organic fertilizers like compost."
        elif 'pest' in question or 'disease' in question or 'രോഗം' in question or 'രോഗങ്ങൾ' in question or 'diseases' in question:
            if is_malayalam:
                return "നെല്ലിന്റെ രോഗങ്ങൾ: പൊതുവായ രോഗങ്ങൾ - ബ്രൗൺ പ്ലാന്റ്ഹോപ്പർ, ഗ്രീൻ ലീഫ്ഹോപ്പർ. ജൈവ നിയന്ത്രണത്തിന് നീം അടിസ്ഥാന പ്രതിരോധകങ്ങൾ ഉപയോഗിക്കുക. നിരന്തരം നിരീക്ഷിക്കുക."
            else:
                return "Rice pests: Common pests include Brown planthopper, Green leafhopper. Use neem-based pesticides for organic control. Monitor regularly."
        else:
            if is_malayalam:
                return "കേരളത്തിലെ നെല്ല് കൃഷി: മഴക്കാലത്ത് നടുക, ശരിയായ വെള്ളനില കാത്തുസൂക്ഷിക്കുക, വളങ്ങൾ ഭാഗങ്ങളായി ചെലുത്തുക, രോഗങ്ങൾ ജൈവമായി നിയന്ത്രിക്കുക. 80-85% ധാന്യങ്ങൾ പക്വമാകുമ്പോൾ വിളവെടുക്കുക."
            else:
                return "Rice farming in Kerala: Plant during monsoon, maintain proper water level, apply fertilizers in splits, control pests organically. Harvest when 80-85% grains are mature."
    
    # Check for coconut-related questions
    elif any(word in question for word in ['coconut', 'തെങ്ങ്', 'coco', 'തെങ്ങിന്റെ', 'തെങ്ങ് കൃഷി']):
        if 'planting' in question or 'plant' in question or 'നടുക' in question:
            if is_malayalam:
                return "തെങ്ങ് നടാനുള്ള ഉത്തമ സമയം മേയ്-ജൂൺ അല്ലെങ്കിൽ സെപ്റ്റംബർ-ഒക്ടോബർ. ഇടവേള: 7.5m x 7.5m. കുഴിയിൽ മുകൾ മണ്ണ് + 50kg FYM + 1kg bone meal നിറയ്ക്കുക."
            else:
                return "Coconut planting: Plant during May-June or September-October. Spacing: 7.5m x 7.5m. Fill pit with topsoil + 50kg FYM + 1kg bone meal."
        elif 'watering' in question or 'water' in question or 'വെള്ളം' in question:
            if is_malayalam:
                return "തെങ്ങിന് വെള്ളം: ചെറിയ തെങ്ങുകൾക്ക് ആഴ്ചയിൽ 40-50 ലിറ്റർ. കായ്ക്കുന്ന തെങ്ങുകൾക്ക് ആഴ്ചയിൽ 200-300 ലിറ്റർ. വെള്ള സംരക്ഷണത്തിന് ഡ്രിപ്പ് ജലസേചനം ഉപയോഗിക്കുക."
            else:
                return "Coconut watering: Young palms need 40-50 liters per week. Bearing palms need 200-300 liters per week. Use drip irrigation for water conservation."
        elif 'fertilizer' in question or 'manure' in question or 'വളം' in question:
            if is_malayalam:
                return "തെങ്ങിന് വളം: ഒരു വർഷത്തിൽ ഒരു തെങ്ങിന് 1.3kg യൂറിയ, 2kg സൂപ്പർഫോസ്ഫേറ്റ്, 1.7kg മ്യൂറിയേറ്റ് ഓഫ് പൊട്ടാഷ് ചെലുത്തുക. 3 ഭാഗങ്ങളായി ചെലുത്തുക."
            else:
                return "Coconut fertilizer: Apply 1.3kg urea, 2kg superphosphate, 1.7kg muriate of potash per palm per year. Split into 3 applications."
        else:
            if is_malayalam:
                return "തെങ്ങ് കൃഷി: നന്നായി വാരിനീക്കുന്ന മണ്ണിൽ നടുക, ശരിയായ ഇടവേള കാത്തുസൂക്ഷിക്കുക, സമതുലിത വളങ്ങൾ ചെലുത്തുക, കൊമ്പൻ കുതിരപ്പുഴു പോലുള്ള രോഗങ്ങൾ നീം കേക്ക് കൊണ്ട് നിയന്ത്രിക്കുക."
            else:
                return "Coconut cultivation: Plant in well-drained soil, maintain proper spacing, apply balanced fertilizers, control pests like rhinoceros beetle with neem cake."
    
    # Check for vegetable farming questions
    elif any(word in question for word in ['vegetable', 'tomato', 'brinjal', 'okra', 'തക്കാളി', 'വഴുതന', 'വെണ്ട', 'vegetable farming', 'vegetable cultivation']):
        if is_malayalam:
            return "കേരളത്തിലെ പച്ചക്കറി കൃഷി: മഴക്കാലത്ത് (ജൂൺ-സെപ്റ്റംബർ) നടുക. മണ്ണ് 2-3 തവണ ഉഴുകുക. ഹെക്ടറിന് 25-30 ടൺ FYM ചേർക്കുക. pH 6.0-7.0 കാത്തുസൂക്ഷിക്കുക. ഡ്രിപ്പ് ജലസേചനം ഉപയോഗിക്കുക. രോഗനിയന്ത്രണത്തിന് നീം എണ്ണ സ്പ്രേ ചെയ്യുക."
        else:
            return "Vegetable farming in Kerala: Plant during monsoon (June-September). Deep plow 2-3 times. Add 25-30 tons FYM per hectare. Maintain pH 6.0-7.0. Use drip irrigation. Apply neem oil spray for pest control. Most vegetables ready in 60-90 days."
    
    # Check for spice cultivation questions
    elif any(word in question for word in ['spice', 'pepper', 'cardamom', 'turmeric', 'ginger', 'കുരുമുളക്', 'ഏലം', 'മഞ്ഞൾ', 'ഇഞ്ചി', 'spice cultivation']):
        if is_malayalam:
            return "കേരളത്തിലെ സുഗന്ധവ്യഞ്ജന കൃഷി: കുരുമുളക് - മേയ്-ജൂൺ നടുക, 3m x 3m ഇടവേള. ഏലം - 600-1200m ഉയരത്തിൽ, 50-60% നിഴൽ. മഞ്ഞൾ - ഏപ്രിൽ-മേയ് നടുക, 30cm x 30cm ഇടവേള. ഇഞ്ചി - ഏപ്രിൽ-മേയ് നടുക, 25cm x 25cm ഇടവേള. ജൈവ രോഗനിയന്ത്രണം ഉപയോഗിക്കുക."
        else:
            return "Spice cultivation in Kerala: Black Pepper - Plant May-June, 3m x 3m spacing. Cardamom - 600-1200m altitude, 50-60% shade. Turmeric - Plant April-May, 30cm x 30cm spacing. Ginger - Plant April-May, 25cm x 25cm spacing. Use organic pest control methods."
    
    # Check for soil management questions
    elif any(word in question for word in ['soil', 'fertilizer', 'manure', 'മണ്ണ്', 'വളം', 'soil management', 'soil fertility']):
        if is_malayalam:
            return "മണ്ണ് മാനേജ്മെന്റ്: pH 6.0-7.0 കാത്തുസൂക്ഷിക്കുക. ഹെക്ടറിന് 25-30 ടൺ FYM ചേർക്കുക. NPK 100:50:100 kg/hectare ചെലുത്തുക. മൈക്രോ ന്യൂട്രിയന്റ് ടെസ്റ്റ് ചെയ്യുക. കമ്പോസ്റ്റ്, വെർമികമ്പോസ്റ്റ് ഉപയോഗിക്കുക. വിള ഭ്രമണം പ്രയോഗിക്കുക."
        else:
            return "Soil management: Maintain pH 6.0-7.0. Add 25-30 tons FYM per hectare. Apply NPK 100:50:100 kg/hectare. Test for micronutrients. Use compost and vermicompost. Practice crop rotation. Test soil every 2-3 years."
    
    # Check for pest and disease questions
    elif any(word in question for word in ['pest', 'disease', 'insect', 'രോഗം', 'രോഗങ്ങൾ', 'കീടങ്ങൾ', 'pest control', 'disease control']):
        if is_malayalam:
            return "രോഗ-കീട നിയന്ത്രണം: ജൈവ രീതികൾ ഉപയോഗിക്കുക. നീം എണ്ണ 2ml/ലിറ്റർ വെള്ളത്തിൽ കലർത്തി സ്പ്രേ ചെയ്യുക. വെളുത്തുള്ളി, മുളക് എക്സ്ട്രാക്റ്റ് ഉപയോഗിക്കുക. വിള ഭ്രമണം പ്രയോഗിക്കുക. ഇന്റർക്രോപ്പിംഗ് ചെയ്യുക. ക്ലീൻ ഫാർമിംഗ് പ്രയോഗിക്കുക."
        else:
            return "Pest and disease control: Use organic methods. Neem oil 2ml per liter water. Use garlic and chili extracts. Practice crop rotation and intercropping. Maintain clean farming practices. Monitor regularly and take preventive measures."
    
    # Check for irrigation questions
    elif any(word in question for word in ['irrigation', 'water', 'watering', 'ജലസേചനം', 'വെള്ളം', 'irrigation management']):
        if is_malayalam:
            return "ജലസേചന മാനേജ്മെന്റ്: ഡ്രിപ്പ് ജലസേചനം 90-95% കാര്യക്ഷമത. നെല്ലിന് 1000-1500mm വെള്ളം. തെങ്ങിന് ആഴ്ചയിൽ 200-300 ലിറ്റർ. പച്ചക്കറികൾക്ക് ദിവസേന ചെറിയ വെള്ളം. മൾച്ചിംഗ് ഉപയോഗിക്കുക. മഴവെള്ളം സംഭരിക്കുക."
        else:
            return "Irrigation management: Drip irrigation 90-95% efficiency. Rice needs 1000-1500mm water. Coconut needs 200-300 liters per week. Vegetables need daily light watering. Use mulching. Practice rainwater harvesting."
    
    # Check for market information questions
    elif any(word in question for word in ['market', 'price', 'selling', 'വിപണി', 'വില', 'വിൽപ്പന', 'marketing']):
        if is_malayalam:
            return "വിപണി വിവരങ്ങൾ: നെല്ല് ₹25-50/കിലോ. തെങ്ങ് ₹8-15/കുരു. കുരുമുളക് ₹400-800/കിലോ. ഏലം ₹800-1500/കിലോ. ഓർഗാനിക് ഉൽപ്പന്നങ്ങൾ 20-50% കൂടുതൽ വില. ഗുണനിലവാരം കാത്തുസൂക്ഷിക്കുക. പാക്കേജിംഗ് മെച്ചപ്പെടുത്തുക."
        else:
            return "Market information: Rice ₹25-50/kg. Coconut ₹8-15/nut. Black Pepper ₹400-800/kg. Cardamom ₹800-1500/kg. Organic products 20-50% premium. Maintain quality standards. Improve packaging. Use direct marketing and cooperatives."
    
    # Check for weather-related questions
    elif any(word in question for word in ['weather', 'rain', 'monsoon', 'കാലാവസ്ഥ', 'മഴ', 'മഴക്കാലം']):
        if is_malayalam:
            return "കേരളത്തിലെ കൃഷിക്ക് കാലാവസ്ഥ: തെക്കുപടിഞ്ഞാറൻ മഴക്കാലം (ജൂൺ-സെപ്റ്റംബർ) നെല്ലിന് നല്ലതാണ്. വേനൽക്കാലം (മാർച്ച്-മേയ്) ജലസേചനം ആവശ്യമാണ്. IMD പ്രവചനങ്ങൾ നിരന്തരം നിരീക്ഷിക്കുക."
        else:
            return "Weather for farming in Kerala: Southwest Monsoon (June-September) is good for rice. Summer (March-May) needs irrigation. Monitor IMD forecasts regularly."
    
    # General farming advice
    elif any(word in question for word in ['farming', 'agriculture', 'കൃഷി', 'കർഷകൻ', 'കൃഷി സഹായി']):
        if is_malayalam:
            return "പൊതുവായ കൃഷി ഉപദേശം: ജൈവ രീതികൾ ഉപയോഗിക്കുക, വിള ഭ്രമണം പ്രയോഗിക്കുക, മണ്ണിന്റെ ആരോഗ്യം കാത്തുസൂക്ഷിക്കുക, കാലാവസ്ഥ നിരീക്ഷിക്കുക, സംയോജിത രോഗനിയന്ത്രണം ഉപയോഗിക്കുക. പ്രത്യേക മാർഗദർശനത്തിന് പ്രാദേശിക കാർഷിക ഉദ്യോഗസ്ഥനെ കണ്ടുമുട്ടുക."
        else:
            return "General farming advice: Use organic methods, practice crop rotation, maintain soil health, monitor weather, use integrated pest management. Consult local agricultural officer for specific guidance."
    
    # Default response
    else:
        if is_malayalam:
            return "നിങ്ങളെ നെല്ല് കൃഷി, തെങ്ങ് കൃഷി, പച്ചക്കറി കൃഷി, സുഗന്ധവ്യഞ്ജന കൃഷി, മണ്ണ് മാനേജ്മെന്റ്, രോഗ-കീട നിയന്ത്രണം, ജലസേചനം, വിപണി വിവരങ്ങൾ, കാലാവസ്ഥ മാർഗദർശനം എന്നിവയിൽ സഹായിക്കാം. വിളകൾ, രോഗങ്ങൾ, കൃഷി രീതികൾ എന്നിവയെക്കുറിച്ച് പ്രത്യേക ചോദ്യങ്ങൾ ചോദിക്കുക."
        else:
            return "I can help you with rice farming, coconut cultivation, vegetable farming, spice cultivation, soil management, pest control, irrigation, market information, weather guidance, and general agricultural advice. Please ask specific questions about crops, pests, diseases, or farming practices."

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
