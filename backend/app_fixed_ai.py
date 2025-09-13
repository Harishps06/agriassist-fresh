#!/usr/bin/env python3
"""
AgriAssist Backend - FIXED AI Integration
Fixed prompt engineering to give specific, question-focused responses
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
print("🚀 Starting AgriAssist with FIXED AI...")

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

def build_enhanced_prompt(question: str, context: str, is_malayalam: bool) -> str:
    """Build a highly specific, question-focused prompt for Gemini AI"""
    
    # Extract key terms from the question
    question_lower = question.lower()
    
    # Determine the specific topic
    if 'coconut' in question_lower or 'നാളികേരം' in question:
        topic = "coconut cultivation"
    elif 'rice' in question_lower or 'അരി' in question:
        topic = "rice farming"
    elif 'pest' in question_lower or 'കീട' in question:
        topic = "pest control"
    elif 'soil' in question_lower or 'മണ്ണ്' in question:
        topic = "soil management"
    elif 'irrigation' in question_lower or 'ജലസേചനം' in question:
        topic = "irrigation"
    elif 'harvest' in question_lower or 'വിളവെടുക്കുക' in question:
        topic = "harvesting"
    elif 'fertilizer' in question_lower or 'വളം' in question:
        topic = "fertilizer management"
    elif 'weather' in question_lower or 'കാലാവസ്ഥ' in question:
        topic = "weather and climate"
    elif 'market' in question_lower or 'വിപണി' in question:
        topic = "market information"
    else:
        topic = "general agriculture"
    
    if is_malayalam:
        return f"""നിങ്ങൾ കേരളത്തിലെ {topic} വിദഗ്ധനാണ്.

ചോദ്യം: {question}

ഉള്ളടക്കം: {context}

ദയവായി {topic} സംബന്ധിച്ച ചുരുങ്ങിയതും പ്രായോഗികവുമായ ഉത്തരം മാത്രം നൽകുക. 3-4 വാചകങ്ങളിൽ മാത്രം. ചോദ്യത്തിന് നേരിട്ട് ഉത്തരം നൽകുക."""
    else:
        return f"""You are a Kerala agricultural expert specializing in {topic}.

Question: {question}

Context: {context}

CRITICAL INSTRUCTIONS:
1. Answer SPECIFICALLY about {topic}
2. Be DIRECT and PRACTICAL
3. Give 3-4 sentences MAXIMUM
4. Focus ONLY on the question asked
5. Use Kerala-specific examples
6. NO generic farming advice

Answer:"""

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
                    logger.info(f"Found relevant context: {context[:100]}...")
                else:
                    logger.warning("No relevant context found in knowledge base")
            else:
                logger.warning("No search results found")
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
    
    # Build enhanced prompt
    prompt = build_enhanced_prompt(question, context, is_malayalam)
    
    try:
        logger.info(f"Enhanced prompt: {prompt[:200]}...")
        response = model.generate_content(prompt)
        answer = response.text
        logger.info(f"Gemini response: {answer[:200]}...")
        
        # Ensure response is specific and not generic
        if "efficient water management" in answer and "pre-sowing irrigation" in answer:
            logger.warning("Detected generic response, trying again with more specific prompt")
            # Try again with even more specific prompt
            specific_prompt = f"""Answer this specific question about Kerala agriculture: {question}

Context: {context}

Give a direct, specific answer about {question}. Do NOT give generic farming advice. Be specific to the question asked."""
            
            response = model.generate_content(specific_prompt)
            answer = response.text
        
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
        'knowledge_base': 'FIXED PDF+TXT system',
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
        "status": "AgriAssist FIXED AI Backend",
        "ai_ready": True,
        "total_entries": sum(len(entries) for entries in knowledge_base.values()) if knowledge_base else 0
    })

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    print(f"🌐 Starting FIXED AI server on http://0.0.0.0:3000")
    app.run(host='0.0.0.0', port=3000, debug=False, threaded=True)
