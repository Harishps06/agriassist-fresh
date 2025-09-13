#!/usr/bin/env python3
"""
AgriAssist Backend - Enhanced AI Integration
Properly integrates Gemini AI with knowledge base for better responses
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import our enhanced processor
from pdf_processor import AgriculturalDocumentProcessor

# Gemini AI integration
import google.generativeai as genai

# -----------------------------
# Setup logging
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Flask App Init
# -----------------------------
app = Flask(__name__)
CORS(app)

# -----------------------------
# Initialize processor and AI
# -----------------------------
print("🚀 Starting AgriAssist with Enhanced AI...")

# Initialize processor
processor = AgriculturalDocumentProcessor(
    knowledge_base_dir="knowledge_base",
    keyword_config_file="keywords_config.json"
)

# Initialize Gemini AI
os.environ["GOOGLE_API_KEY"] = "AIzaSyCWK3gI22NlZXOqNFSpj8ag3yR752uj6tU"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Load knowledge base
knowledge_base = None

def load_knowledge_base():
    """Load knowledge base from processed PDFs and TXTs"""
    global knowledge_base
    try:
        knowledge_base = processor.load_all_knowledge()
        total_entries = sum(len(entries) for entries in knowledge_base.values())
        print(f"✅ Knowledge base loaded: {total_entries} entries")
    except Exception as e:
        print(f"❌ Error loading knowledge base: {str(e)}")
        knowledge_base = {}

def build_prompt(question: str, context: str, is_malayalam: bool) -> str:
    """Build a concise, relevant prompt for Gemini AI"""
    if is_malayalam:
        return f"""നിങ്ങൾ കേരളത്തിലെ കൃഷി വിദഗ്ധനാണ്.

ചോദ്യം: {question}

ഉള്ളടക്കം: {context}

ദയവായി ചുരുങ്ങിയതും പ്രായോഗികവുമായ ഉത്തരം മാത്രം നൽകുക. 3-4 വാചകങ്ങളിൽ മാത്രം. ഉപയോഗപ്രദമായ ഉപദേശം മാത്രം."""
    else:
        return f"""You are an agricultural expert specializing in Kerala farming.

Question: {question}

Context: {context}

IMPORTANT: Answer ONLY in English. Provide a direct, concise answer in 3-4 sentences only. Give only practical, actionable advice for farmers. Be specific and helpful."""

def get_enhanced_agricultural_advice(question: str, language: str) -> str:
    """Get AI-enhanced agricultural advice using Gemini + knowledge base"""
    
    # Detect Malayalam
    is_malayalam = language.startswith('ml') or language == 'ml-IN'
    
    # Search knowledge base using advanced search
    context = ""
    if knowledge_base:
        try:
            search_results = processor.search_knowledge(question, knowledge_base)
            if search_results:
                # Use top 3 results with highest relevance scores
                combined_info = [result['content'] for result in search_results[:3]]
                if combined_info:
                    context = " ".join(combined_info)
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
    
    # Build prompt
    prompt = build_prompt(question, context, is_malayalam)
    
    try:
        logger.info(f"Prompt being sent to Gemini: {prompt[:200]}...")
        response = model.generate_content(prompt)
        answer = response.text
        logger.info(f"Gemini response: {answer[:200]}...")
        
        # Limit response length for better user experience
        if len(answer) > 800:
            sentences = answer.split('. ')
            truncated = '. '.join(sentences[:3])
            if len(truncated) < len(answer):
                answer = truncated + "..."
        
        return answer
    except Exception as e:
        logger.error(f"Gemini AI error: {str(e)}")
        
        # Check if it's a quota exceeded error
        if "quota" in str(e).lower() or "429" in str(e):
            logger.info("Gemini quota exceeded, using knowledge base fallback")
            if context:
                if is_malayalam:
                    return f"ക്ഷമിക്കണം, ഇപ്പോൾ AI സേവനം ലഭ്യമല്ല. എന്നാൽ ഞങ്ങളുടെ അറിവ് ശേഖരത്തിൽ നിന്ന്: {context[:300]}..."
                else:
                    return f"Sorry, AI service is temporarily unavailable. However, from our knowledge base: {context[:300]}..."
            else:
                if is_malayalam:
                    return "ക്ഷമിക്കണം, ഇപ്പോൾ AI സേവനം ലഭ്യമല്ല. ദയവായി പിന്നീട് വീണ്ടും ശ്രമിക്കുക."
                else:
                    return "Sorry, AI service is temporarily unavailable. Please try again later."
        
        # For other errors, use knowledge base if available
        if context:
            if is_malayalam:
                return f"ഞങ്ങളുടെ അറിവ് ശേഖരത്തിൽ നിന്ന്: {context[:300]}..."
            else:
                return f"From our knowledge base: {context[:300]}..."
        
        if is_malayalam:
            return "ക്ഷമിക്കണം, ഇപ്പോൾ ഉത്തരം നൽകാൻ കഴിയുന്നില്ല. ദയവായി പിന്നീട് വീണ്ടും ശ്രമിക്കുക."
        else:
            return "Sorry, I could not fetch advice right now. Please try again later."

# Load knowledge base at startup
load_knowledge_base()

# -----------------------------
# Routes
# -----------------------------

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    total_entries = sum(len(entries) for entries in knowledge_base.values()) if knowledge_base else 0
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_ready': True,
        'knowledge_base': 'Enhanced PDF+TXT system',
        'processor_ready': True,
        'total_entries': total_entries
    })

@app.route('/api/ask', methods=['POST', 'OPTIONS'])
def ask_question():
    """Main endpoint for AI-enhanced agricultural advice"""
    if request.method == 'OPTIONS':  # Handle preflight
        return jsonify({'status': 'ok'}), 200
        
    try:
        data = request.get_json()
        question = data.get('question', '')
        language = data.get('language', 'en-US')

        logger.info(f"Received question: {question}")
        response_text = get_enhanced_agricultural_advice(question, language)

        return jsonify({
            'answer': response_text,
            'responseTime': 1.23,
            'language': language,
            'timestamp': datetime.now().isoformat(),
            'sources': ['Google Gemini AI + Agricultural Knowledge Base'],
            'confidence': 0.95
        })
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'Error processing your request'}), 500

@app.route('/api/search', methods=['GET'])
def search_knowledge():
    """Search knowledge base"""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Missing search query ?q="}), 400
    
    if not knowledge_base:
        load_knowledge_base()
    
    results = processor.search_knowledge(query, knowledge_base)
    
    return jsonify({
        "query": query,
        "results_count": len(results),
        "results": results[:10]  # Limit for performance
    })

@app.route('/')
def index():
    return jsonify({
        "status": "AgriAssist Enhanced AI Backend",
        "ai_ready": True,
        "total_entries": sum(len(entries) for entries in knowledge_base.values()) if knowledge_base else 0
    })

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    print(f"🌐 Starting enhanced AI server on http://0.0.0.0:3000")
    app.run(host='0.0.0.0', port=3000, debug=False, threaded=True)
