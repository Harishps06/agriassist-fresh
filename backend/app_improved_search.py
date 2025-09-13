#!/usr/bin/env python3
"""
AgriAssist Backend - Improved Search
Better search algorithm and response processing
"""

import os
import logging
import re
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
print("🚀 Starting AgriAssist with Improved Search...")

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

def find_most_relevant_content(question: str, search_results: list) -> str:
    """Find the most relevant content from search results"""
    
    if not search_results:
        return ""
    
    question_lower = question.lower()
    question_words = set(re.findall(r'\b\w+\b', question_lower))
    
    best_content = ""
    best_score = 0
    
    for result in search_results:
        content = result.get('content', '')
        content_lower = content.lower()
        
        # Calculate relevance score
        score = 0
        
        # Exact phrase match gets highest score
        if question_lower in content_lower:
            score += 10
        
        # Word overlap score
        content_words = set(re.findall(r'\b\w+\b', content_lower))
        word_overlap = len(question_words & content_words)
        score += word_overlap * 2
        
        # Length bonus for longer, more detailed content
        if len(content) > 200:
            score += 1
        
        # Check for agricultural keywords
        agri_keywords = ['cultivation', 'farming', 'crop', 'pest', 'disease', 'irrigation', 'fertilizer', 'soil', 'harvest']
        for keyword in agri_keywords:
            if keyword in content_lower:
                score += 1
        
        if score > best_score:
            best_score = score
            best_content = content
    
    return best_content

def process_response_content(content: str, question: str) -> str:
    """Process the content to make it more relevant to the question"""
    
    if not content:
        return ""
    
    # Extract sentences that are most relevant to the question
    sentences = re.split(r'[.!?]+', content)
    question_words = set(re.findall(r'\b\w+\b', question.lower()))
    
    relevant_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 20:  # Skip very short sentences
            continue
            
        sentence_lower = sentence.lower()
        
        # Check if sentence contains question words
        if any(word in sentence_lower for word in question_words):
            relevant_sentences.append(sentence)
        # Also include sentences with agricultural keywords
        elif any(keyword in sentence_lower for keyword in ['cultivation', 'farming', 'crop', 'pest', 'disease', 'irrigation', 'fertilizer', 'soil', 'harvest']):
            relevant_sentences.append(sentence)
    
    # If we found relevant sentences, use them
    if relevant_sentences:
        # Take the first 3 most relevant sentences
        answer = '. '.join(relevant_sentences[:3])
        if not answer.endswith('.'):
            answer += '.'
        return answer
    
    # Fallback: use the first part of the content
    return content[:300] + "..." if len(content) > 300 else content

def get_improved_agricultural_advice(question: str, language: str) -> str:
    """Get agricultural advice using improved search and processing"""
    
    # Detect Malayalam
    is_malayalam = language.startswith('ml') or language == 'ml-IN'
    
    # Search knowledge base
    if not knowledge_base:
        if is_malayalam:
            return "ക്ഷമിക്കണം, അറിവ് ശേഖരം ലോഡ് ചെയ്യാൻ കഴിഞ്ഞില്ല."
        else:
            return "Sorry, knowledge base could not be loaded."
    
    try:
        search_results = processor.search_knowledge(question, knowledge_base)
        logger.info(f"Found {len(search_results)} search results")
        
        if search_results:
            # Find the most relevant content
            relevant_content = find_most_relevant_content(question, search_results)
            logger.info(f"Most relevant content: {relevant_content[:100]}...")
            
            if relevant_content:
                # Process the content to make it more relevant
                processed_content = process_response_content(relevant_content, question)
                
                if processed_content:
                    # Add a helpful prefix
                    if is_malayalam:
                        answer = f"ഞങ്ങളുടെ കൃഷി അറിവ് ശേഖരത്തിൽ നിന്ന്: {processed_content}"
                    else:
                        answer = f"Based on our agricultural knowledge base: {processed_content}"
                    
                    return answer
        
        # No relevant content found
        if is_malayalam:
            return "ക്ഷമിക്കണം, ഈ ചോദ്യത്തിന് ഉത്തരം ഞങ്ങളുടെ അറിവ് ശേഖരത്തിൽ കണ്ടെത്താൻ കഴിഞ്ഞില്ല. ദയവായി വ്യത്യസ്തമായ ചോദ്യം ചോദിക്കുക."
        else:
            return "Sorry, we couldn't find specific information for your question in our knowledge base. Please try asking a different question about Kerala agriculture."
            
    except Exception as e:
        logger.error(f"Error searching knowledge base: {str(e)}")
        if is_malayalam:
            return "ക്ഷമിക്കണം, അറിവ് ശേഖരം തിരയുമ്പോൾ പിശക് സംഭവിച്ചു."
        else:
            return "Sorry, there was an error searching our knowledge base."

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
        'knowledge_base': 'Improved Search System',
        'processor_ready': True,
        'total_entries': total_entries
    })

@app.route('/api/ask', methods=['POST', 'OPTIONS'])
def ask_question():
    """Main endpoint for agricultural advice using improved search"""
    if request.method == 'OPTIONS':  # Handle preflight
        return jsonify({'status': 'ok'}), 200
        
    try:
        data = request.get_json()
        question = data.get('question', '')
        language = data.get('language', 'en-US')

        logger.info(f"Received question: {question}")
        response_text = get_improved_agricultural_advice(question, language)

        return jsonify({
            'answer': response_text,
            'responseTime': 0.5,
            'language': language,
            'timestamp': datetime.now().isoformat(),
            'sources': ['Agricultural Knowledge Base'],
            'confidence': 0.85
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
        "results": results[:10]
    })

@app.route('/')
def index():
    return jsonify({
        "status": "AgriAssist Improved Search Backend",
        "ai_ready": False,
        "total_entries": sum(len(entries) for entries in knowledge_base.values()) if knowledge_base else 0
    })

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    print(f"🌐 Starting Improved Search server on http://0.0.0.0:3000")
    app.run(host='0.0.0.0', port=3000, debug=False, threaded=True)
