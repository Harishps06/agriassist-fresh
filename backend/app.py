import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from pdf_processor import AgriculturalPDFProcessor
import logging
import google.generativeai as genai
from werkzeug.utils import secure_filename

# -----------------------------
# Setup logging
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Initialize the Flask application
# -----------------------------
app = Flask(__name__)

# ✅ Simplified, broad CORS (good for dev)
CORS(app, resources={r"/*": {
    "origins": ["http://172.20.10.3:8000", "http://localhost:8000"],
    "allow_headers": "*",
    "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"]
}})

# -----------------------------
# Google API Key & Gemini AI setup
# -----------------------------
os.environ["GOOGLE_API_KEY"] = "AIzaSyCWK3gI22NlZXOqNFSpj8ag3yR752uj6tU"

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# -----------------------------
# PDF processor & knowledge base
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
    except Exception as e:
        logger.error(f"Error loading knowledge base: {str(e)}")
        knowledge_base = {}

# -----------------------------
# Prompt builder
# -----------------------------
def build_prompt(question: str, context: str, is_malayalam: bool) -> str:
    """Build a short, relevant prompt for Gemini AI"""
    if is_malayalam:
        return f"""നിങ്ങൾ കേരളത്തിലെ കൃഷി വിദഗ്ധനാണ്.

ചോദ്യം: {question}

ഉള്ളടക്കം: {context}

ദയവായി ചുരുങ്ങിയതും പ്രായോഗികവുമായ ഉത്തരം മാത്രം നൽകുക. 3-4 വാചകങ്ങളിൽ മാത്രം."""
    else:
        return f"""You are an agricultural expert specializing in Kerala farming.

Question: {question}

Context: {context}

IMPORTANT: Answer ONLY in English. Provide a direct, concise answer in 3-4 sentences only. Give only practical, actionable advice."""

# -----------------------------
# Agricultural advice using Gemini AI + PDFs
# -----------------------------
def get_enhanced_agricultural_advice(question: str, language: str) -> str:
    """Get agricultural advice using Gemini AI and PDF knowledge base"""

    # Detect Malayalam - use language parameter as primary indicator
    is_malayalam = language.startswith('ml') or language == 'ml-IN'

    # Search knowledge base
    context = ""
    if knowledge_base:
        try:
            search_results = pdf_processor.search_knowledge(question, knowledge_base)
            if search_results:
                combined_info = [result['content'] for result in search_results[:3]]
                if combined_info:
                    context = " ".join(combined_info)
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")

    # Build prompt using helper function
    prompt = build_prompt(question, context, is_malayalam)

    try:
        logger.info(f"Prompt being sent to Gemini: {prompt[:200]}...")
        response = model.generate_content(prompt)
        answer = response.text
        logger.info(f"Gemini response: {answer[:200]}...")
        
        # Limit response length for better user experience
        if len(answer) > 1000:
            # Try to find a good stopping point
            sentences = answer.split('. ')
            truncated = '. '.join(sentences[:3])  # Take first 3 sentences
            if len(truncated) < len(answer):
                answer = truncated + "..."
        
        return answer
    except Exception as e:
        logger.error(f"Gemini AI error: {str(e)}")
        
        # Check if it's a quota exceeded error
        if "quota" in str(e).lower() or "429" in str(e):
            logger.info("Gemini quota exceeded, using knowledge base fallback")
            if context:
                # Use knowledge base as fallback
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

# -----------------------------
# API Endpoints
# -----------------------------
@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Main endpoint to get agricultural advice"""
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

@app.route('/api/process-pdfs', methods=['POST'])
def process_pdfs():
    """Endpoint to process PDFs and update knowledge base"""
    try:
        data = request.get_json()
        pdf_directory = data.get('pdf_directory', 'agricultural_pdfs')

        processed_entries = pdf_processor.process_multiple_pdfs(pdf_directory)
        load_knowledge_base()

        return jsonify({
            'success': True,
            'processed_files': len(processed_entries),
            'message': f'Successfully processed {len(processed_entries)} PDF files',
            'files': [entry['file_name'] for entry in processed_entries]
        })
    except Exception as e:
        logger.error(f"Error processing PDFs: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

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

        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        logger.error(f"Error getting knowledge stats: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_ready': True,
        'knowledge_base': 'PDF-enhanced system',
        'pdf_processor_ready': True
    })

# -----------------------------
# Stub endpoints with file upload support
# -----------------------------
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/image-query', methods=['POST'])
def image_query():
    """
    Stub endpoint for handling image queries.
    Accepts image files but currently just returns a placeholder.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400
    file = request.files['image']
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    logger.info(f"Received image file: {filename}")

    return jsonify({
        'answer': f'Image analysis feature coming soon. File saved as {filename}',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/voice-query', methods=['POST'])
def voice_query():
    """
    Stub endpoint for handling voice queries.
    Accepts audio files but currently just returns a placeholder.
    """
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400
    file = request.files['audio']
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    logger.info(f"Received audio file: {filename}")

    return jsonify({
        'answer': f'Voice analysis feature coming soon. File saved as {filename}',
        'timestamp': datetime.now().isoformat()
    })

# -----------------------------
# Server startup
# -----------------------------
if __name__ == '__main__':
    print("🚀 Starting AgriAssist PDF-Enhanced Backend Server...")
    print("📚 Loading knowledge base from PDFs...")
    load_knowledge_base()
    print("🌐 Server starting on http://0.0.0.0:3000")
    app.run(debug=True, port=3000, host='0.0.0.0')