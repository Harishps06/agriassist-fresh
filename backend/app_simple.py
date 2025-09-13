import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from pdf_processor import AgriculturalPDFProcessor
import logging

# -----------------------------
# Setup logging
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Initialize the Flask application
# -----------------------------
app = Flask(__name__)

# ✅ Enhanced CORS configuration
CORS(app, resources={r"/*": {
    "origins": [
        "http://localhost:8000",
        "http://172.20.10.3:8000",
        "https://agriassist-fresh.onrender.com"
    ]
}})

# ✅ Ensure all responses include proper CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS,PUT,DELETE')
    return response

# -----------------------------
# PDF processor & knowledge base (NO GEMINI)
# -----------------------------
pdf_processor = AgriculturalPDFProcessor("knowledge_base")
knowledge_base = None

# -----------------------------
# Load knowledge base
# -----------------------------
def load_knowledge_base():
    """Load knowledge base from processed PDFs"""
    global knowledge_base
    try:
        knowledge_base = pdf_processor.load_all_knowledge()
        logger.info("Knowledge base loaded successfully")
        logger.info(f"Loaded {sum(len(entries) for entries in knowledge_base.values())} total entries")
    except Exception as e:
        logger.error(f"Error loading knowledge base: {str(e)}")
        knowledge_base = {}

# -----------------------------
# Simple agricultural advice using knowledge base only
# -----------------------------
def get_simple_agricultural_advice(question: str, language: str) -> str:
    """Get agricultural advice using knowledge base only (no Gemini)"""
    is_malayalam = language.startswith('ml') or language == 'ml-IN'
    context = ""
    
    if knowledge_base:
        try:
            search_results = pdf_processor.search_knowledge(question, knowledge_base)
            logger.info(f"Found {len(search_results)} search results for: {question}")
            
            if search_results:
                # Filter results by language preference
                filtered_results = []
                for result in search_results[:5]:
                    content = result['content']
                    has_malayalam_chars = any('\u0D00' <= char <= '\u0D7F' for char in content)
                    has_english_chars = any('a' <= char.lower() <= 'z' for char in content)
                    
                    if is_malayalam and has_malayalam_chars:
                        filtered_results.append(result)
                    elif not is_malayalam and has_english_chars:
                        english_ratio = sum(1 for char in content if 'a' <= char.lower() <= 'z') / len(content) if content else 0
                        if english_ratio > 0.3:
                            filtered_results.append(result)
                    elif not filtered_results:
                        filtered_results.append(result)
                
                logger.info(f"Filtered to {len(filtered_results)} results")
                if filtered_results:
                    combined_info = [result['content'] for result in filtered_results[:3]]
                    context = " ".join(combined_info)
                    logger.info(f"Context length: {len(context)} characters")
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
    
    # Return knowledge base content directly
    if context:
        if is_malayalam:
            return f"ഞങ്ങളുടെ അറിവ് ശേഖരത്തിൽ നിന്ന്: {context[:500]}..."
        else:
            return f"From our knowledge base: {context[:500]}..."
    else:
        if is_malayalam:
            return "ക്ഷമിക്കണം, ഈ ചോദ്യത്തിന് ഉത്തരം കണ്ടെത്താൻ കഴിഞ്ഞില്ല. ദയവായി വ്യത്യസ്ത ചോദ്യം ചോദിക്കുക."
        else:
            return "Sorry, I couldn't find relevant information for this question. Please try asking a different question."

# -----------------------------
# API Endpoints
# -----------------------------
@app.route('/api/ask', methods=['POST', 'OPTIONS'])
def ask_question():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        data = request.get_json()
        question = data.get('question', '')
        language = data.get('language', 'en-US')
        
        logger.info(f"Received question: {question}")
        response_text = get_simple_agricultural_advice(question, language)
        
        return jsonify({
            'answer': response_text,
            'responseTime': 1.23,
            'language': language,
            'timestamp': datetime.now().isoformat(),
            'sources': ['Agricultural Knowledge Base'],
            'confidence': 0.95
        })
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'Error processing your request'}), 500

@app.route('/api/knowledge-stats', methods=['GET'])
def get_knowledge_stats():
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
        
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        logger.error(f"Error getting knowledge stats: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_ready': False,  # No Gemini AI
        'knowledge_base': 'PDF-enhanced system',
        'pdf_processor_ready': True
    })

# -----------------------------
# Server startup
# -----------------------------
if __name__ == '__main__':
    print("🚀 Starting AgriAssist Simplified Backend Server...")
    print("📚 Loading knowledge base from PDFs...")
    load_knowledge_base()
    print("🌐 Server starting on http://0.0.0.0:3000")
    print("⚠️  Note: This is a simplified version without Gemini AI")
    app.run(debug=True, port=3000, host='0.0.0.0')
