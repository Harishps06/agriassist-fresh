#!/usr/bin/env python3
"""
AgriAssist Backend - Knowledge Base Only
Uses only knowledge base for responses (no Gemini AI)
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import our enhanced processor
from pdf_processor import AgriculturalDocumentProcessor

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
# Initialize processor
# -----------------------------
print("🚀 Starting AgriAssist with Knowledge Base Only...")

# Initialize processor
processor = AgriculturalDocumentProcessor(
    knowledge_base_dir="knowledge_base",
    keyword_config_file="keywords_config.json"
)

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

def get_knowledge_based_advice(question: str, language: str) -> str:
    """Get agricultural advice using only knowledge base"""
    
    # Detect Malayalam
    is_malayalam = language.startswith('ml') or language == 'ml-IN'
    
    # Search knowledge base
    context = ""
    if knowledge_base:
        try:
            search_results = processor.search_knowledge(question, knowledge_base)
            if search_results:
                # Use top 3 results with highest relevance scores
                combined_info = [result['content'] for result in search_results[:3]]
                if combined_info:
                    context = " ".join(combined_info)
                    logger.info(f"Found relevant context: {context[:100]}...")
                else:
                    logger.warning("No relevant context found in knowledge base")
            else:
                logger.warning("No search results found")
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
    
    # Process the context to give a better response
    if context:
        # Extract the most relevant sentences
        sentences = context.split('. ')
        relevant_sentences = []
        
        # Look for sentences that contain keywords from the question
        question_words = question.lower().split()
        
        for sentence in sentences:
            if any(word in sentence.lower() for word in question_words):
                relevant_sentences.append(sentence)
        
        # If we found relevant sentences, use them
        if relevant_sentences:
            # Take the first 3 relevant sentences
            answer = '. '.join(relevant_sentences[:3])
            if not answer.endswith('.'):
                answer += '.'
        else:
            # Use the first part of the context
            answer = context[:300] + "..." if len(context) > 300 else context
        
        # Add a helpful prefix
        if is_malayalam:
            answer = f"ഞങ്ങളുടെ കൃഷി അറിവ് ശേഖരത്തിൽ നിന്ന്: {answer}"
        else:
            answer = f"Based on our agricultural knowledge base: {answer}"
        
        return answer
    else:
        # No context found
        if is_malayalam:
            return "ക്ഷമിക്കണം, ഈ ചോദ്യത്തിന് ഉത്തരം ഞങ്ങളുടെ അറിവ് ശേഖരത്തിൽ കണ്ടെത്താൻ കഴിഞ്ഞില്ല. ദയവായി വ്യത്യസ്തമായ ചോദ്യം ചോദിക്കുക."
        else:
            return "Sorry, we couldn't find specific information for your question in our knowledge base. Please try asking a different question about Kerala agriculture."

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
        'ai_ready': False,  # No AI, only knowledge base
        'knowledge_base': 'Knowledge Base Only System',
        'processor_ready': True,
        'total_entries': total_entries
    })

@app.route('/api/ask', methods=['POST', 'OPTIONS'])
def ask_question():
    """Main endpoint for agricultural advice using knowledge base only"""
    if request.method == 'OPTIONS':  # Handle preflight
        return jsonify({'status': 'ok'}), 200
        
    try:
        data = request.get_json()
        question = data.get('question', '')
        language = data.get('language', 'en-US')

        logger.info(f"Received question: {question}")
        response_text = get_knowledge_based_advice(question, language)

        return jsonify({
            'answer': response_text,
            'responseTime': 0.5,  # Faster since no AI call
            'language': language,
            'timestamp': datetime.now().isoformat(),
            'sources': ['Agricultural Knowledge Base'],
            'confidence': 0.85  # Slightly lower confidence since no AI
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
        "status": "AgriAssist Knowledge Base Only Backend",
        "ai_ready": False,
        "total_entries": sum(len(entries) for entries in knowledge_base.values()) if knowledge_base else 0
    })

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    print(f"🌐 Starting Knowledge Base Only server on http://0.0.0.0:3000")
    app.run(host='0.0.0.0', port=3000, debug=False, threaded=True)
