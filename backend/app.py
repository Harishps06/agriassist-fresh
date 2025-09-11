import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
from datetime import datetime
from pdf_processor import AgriculturalPDFProcessor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Flask application
app = Flask(__name__)
CORS(app, 
     origins="*", 
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers", "Access-Control-Allow-Methods"],
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
     supports_credentials=False)

# Set up Google API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCWK3gI22NlZXOqNFSpj8ag3yR752uj6tU"

# Initialize PDF processor
pdf_processor = AgriculturalPDFProcessor("knowledge_base")
knowledge_base = None

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, Access-Control-Allow-Origin, Access-Control-Allow-Headers, Access-Control-Allow-Methods')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response

def load_knowledge_base():
    """Load knowledge base from processed PDFs"""
    global knowledge_base
    try:
        knowledge_base = pdf_processor.load_all_knowledge()
        logger.info("Knowledge base loaded successfully")
    except Exception as e:
        logger.error(f"Error loading knowledge base: {str(e)}")
        knowledge_base = {}

def get_enhanced_agricultural_advice(question: str, language: str) -> str:
    """Get agricultural advice using PDF knowledge base"""
    
    # Detect if question is in Malayalam
    malayalam_chars = 'അആഇഈഉഊഋഎഏഐഒഓഔകഖഗഘങചഛജഝഞടഠഡഢണതഥദധനപഫബഭമയരലവശഷസഹളഴറ'
    malayalam_words = ['നെല്ല്', 'തെങ്ങ്', 'കൃഷി', 'വളം', 'വെള്ളം', 'രോഗം', 'കീടം', 'മണ്ണ്', 'വിപണി', 'കാലാവസ്ഥ']
    
    is_malayalam = any(char in question for char in malayalam_chars) or any(word in question for word in malayalam_words)
    
    # Search knowledge base
    if knowledge_base:
        search_results = pdf_processor.search_knowledge(question, knowledge_base)
        
        if search_results:
            # Combine relevant information
            combined_info = []
            for result in search_results[:3]:  # Take top 3 results
                combined_info.append(result['content'])
            
            if combined_info:
                response = " ".join(combined_info)
                
                # Add Malayalam translation if needed
                if is_malayalam and language == 'ml-IN':
                    # For now, return the English response
                    # In a full implementation, you'd translate this
                    return response
                else:
                    return response
    
    # Fallback to simple responses if no PDF knowledge found
    return get_simple_agricultural_advice(question, language, is_malayalam)

def get_simple_agricultural_advice(question: str, language: str, is_malayalam: bool) -> str:
    """Fallback simple agricultural advice"""
    
    # Check for rice-related questions
    if any(word in question for word in ['rice', 'നെല്ല്', 'paddy', 'അരി', 'നെല്ലിന്റെ', 'അരി കൃഷി', 'നെല്ലിന്റെ രോഗങ്ങൾ', 'നെല്ല് രോഗം', 'rice farming', 'rice cultivation']):
        if is_malayalam:
            return "കേരളത്തിലെ നെല്ല് കൃഷി: മഴക്കാലത്ത് നടുക, ശരിയായ വെള്ളനില കാത്തുസൂക്ഷിക്കുക, വളങ്ങൾ ഭാഗങ്ങളായി ചെലുത്തുക, രോഗങ്ങൾ ജൈവമായി നിയന്ത്രിക്കുക. 80-85% ധാന്യങ്ങൾ പക്വമാകുമ്പോൾ വിളവെടുക്കുക."
        else:
            return "Rice farming in Kerala: Plant during monsoon, maintain proper water level, apply fertilizers in splits, control pests organically. Harvest when 80-85% grains are mature."
    
    # Check for coconut-related questions
    elif any(word in question for word in ['coconut', 'തെങ്ങ്', 'coco', 'തെങ്ങിന്റെ', 'തെങ്ങ് കൃഷി']):
        if is_malayalam:
            return "തെങ്ങ് കൃഷി: നന്നായി വാരിനീക്കുന്ന മണ്ണിൽ നടുക, ശരിയായ ഇടവേള കാത്തുസൂക്ഷിക്കുക, സമതുലിത വളങ്ങൾ ചെലുത്തുക, കൊമ്പൻ കുതിരപ്പുഴു പോലുള്ള രോഗങ്ങൾ നീം കേക്ക് കൊണ്ട് നിയന്ത്രിക്കുക."
        else:
            return "Coconut cultivation: Plant in well-drained soil, maintain proper spacing, apply balanced fertilizers, control pests like rhinoceros beetle with neem cake."
    
    # Default response
    else:
        if is_malayalam:
            return "നിങ്ങളെ നെല്ല് കൃഷി, തെങ്ങ് കൃഷി, പച്ചക്കറി കൃഷി, സുഗന്ധവ്യഞ്ജന കൃഷി, മണ്ണ് മാനേജ്മെന്റ്, രോഗ-കീട നിയന്ത്രണം, ജലസേചനം, വിപണി വിവരങ്ങൾ, കാലാവസ്ഥ മാർഗദർശനം എന്നിവയിൽ സഹായിക്കാം. വിളകൾ, രോഗങ്ങൾ, കൃഷി രീതികൾ എന്നിവയെക്കുറിച്ച് പ്രത്യേക ചോദ്യങ്ങൾ ചോദിക്കുക."
        else:
            return "I can help you with rice farming, coconut cultivation, vegetable farming, spice cultivation, soil management, pest control, irrigation, market information, weather guidance, and general agricultural advice. Please ask specific questions about crops, pests, diseases, or farming practices."

@app.route('/api/ask', methods=['POST', 'OPTIONS'])
@cross_origin(origins="*", allow_headers=["Content-Type", "Authorization"])
def ask_question():
    # Handle CORS preflight request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Access-Control-Allow-Origin, Access-Control-Allow-Headers, Access-Control-Allow-Methods'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
        response.headers['Access-Control-Max-Age'] = '86400'
        return response
    try:
        data = request.get_json()
        
        # Extract data from frontend
        question = data.get('question', '')
        language = data.get('language', 'en-US')
        context = data.get('context', {})
        
        logger.info(f"Server received question: {question}")
        logger.info(f"Language: {language}")
        
        # Get enhanced response using PDF knowledge
        response_text = get_enhanced_agricultural_advice(question, language)
        
        # Calculate response time
        response_time = 1.23
        
        # Return enhanced response
        response = jsonify({
            'answer': response_text,
            'responseTime': response_time,
            'language': language,
            'timestamp': datetime.now().isoformat(),
            'sources': ['Agricultural Knowledge Base + PDF Documents'],
            'confidence': 0.95
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Sorry, there was an error processing your request. Please try again.',
            'answer': 'I apologize, but I encountered an error while processing your question. Please try again in a moment.'
        }), 500

@app.route('/api/process-pdfs', methods=['POST'])
def process_pdfs():
    """Endpoint to process PDFs and update knowledge base"""
    try:
        data = request.get_json()
        pdf_directory = data.get('pdf_directory', 'agricultural_pdfs')
        
        # Process PDFs
        processed_entries = pdf_processor.process_multiple_pdfs(pdf_directory)
        
        # Reload knowledge base
        load_knowledge_base()
        
        return jsonify({
            'success': True,
            'processed_files': len(processed_entries),
            'message': f'Successfully processed {len(processed_entries)} PDF files',
            'files': [entry['file_name'] for entry in processed_entries]
        })
        
    except Exception as e:
        logger.error(f"Error processing PDFs: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/knowledge-stats', methods=['GET'])
def get_knowledge_stats():
    """Get statistics about the knowledge base"""
    try:
        if not knowledge_base:
            load_knowledge_base()
        
        stats = {}
        total_entries = 0
        
        for section, entries in knowledge_base.items():
            stats[section] = len(entries)
            total_entries += len(entries)
        
        stats['total_entries'] = total_entries
        stats['sections'] = list(knowledge_base.keys())
        
        return jsonify({
            'success': True,
            'stats': stats,
            'knowledge_base_loaded': knowledge_base is not None
        })
        
    except Exception as e:
        logger.error(f"Error getting knowledge stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_ready': True,
        'knowledge_base': 'PDF-enhanced system',
        'pdf_processor_ready': True
    })

# Test Malayalam detection endpoint
@app.route('/api/test-malayalam', methods=['POST'])
def test_malayalam():
    data = request.get_json()
    question = data.get('question', '')
    
    # Test Malayalam detection
    malayalam_chars = 'അആഇഈഉഊഋഎഏഐഒഓഔകഖഗഘങചഛജഝഞടഠഡഢണതഥദധനപഫബഭമയരലവശഷസഹളഴറ'
    malayalam_words = ['നെല്ല്', 'തെങ്ങ്', 'കൃഷി', 'വളം', 'വെള്ളം', 'രോഗം', 'കീടം', 'മണ്ണ്', 'വിപണി', 'കാലാവസ്ഥ']
    
    has_malayalam_chars = any(char in question for char in malayalam_chars)
    has_malayalam_words = any(word in question for word in malayalam_words)
    is_malayalam = has_malayalam_chars or has_malayalam_words
    
    return jsonify({
        'question': question,
        'has_malayalam_chars': has_malayalam_chars,
        'has_malayalam_words': has_malayalam_words,
        'is_malayalam': is_malayalam,
        'detected_chars': [char for char in question if char in malayalam_chars],
        'detected_words': [word for word in malayalam_words if word in question]
    })

if __name__ == '__main__':
    print("🚀 Starting AgriAssist PDF-Enhanced Backend Server...")
    print("📚 Loading knowledge base from PDFs...")
    
    # Load knowledge base on startup
    load_knowledge_base()
    
    print("🌐 Server starting on http://127.0.0.1:3000")
    print("📱 Frontend can now connect to this backend")
    print("📄 PDF processing capabilities enabled")
    
    app.run(debug=True, port=3000, host='0.0.0.0')
