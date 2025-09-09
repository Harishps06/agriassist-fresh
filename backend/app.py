import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

# --- NEW IMPORTS FOR THE AI BRAIN ---
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # This allows your frontend to connect

# --- SETUP THE AI BRAIN (This runs only once when the server starts) ---

# 1. Put your Google API Key here
os.environ["GOOGLE_API_KEY"] = "AIzaSyCWK3gI22NlZXOqNFSpj8ag3yR752uj6tU"

# 2. Load the documents from your knowledge_base folder
pdf_loader = DirectoryLoader('./knowledge_base/', glob="**/*.pdf", loader_cls=PyPDFLoader)
txt_loader = DirectoryLoader('./knowledge_base/', glob="**/*.txt", loader_cls=TextLoader)
pdf_documents = pdf_loader.load()
txt_documents = txt_loader.load()
documents = pdf_documents + txt_documents

# 3. Split the documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# 4. Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 5. Create a Vector Store
vector_store = Chroma.from_documents(texts, embeddings, persist_directory="db")
vector_store.persist()
vector_store = None

# 6. Setup the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.2, convert_system_message_to_human=True)
qa_chain = None

# --- END OF AI SETUP ---

# Enhanced API endpoint that works with your frontend
@app.route('/api/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        
        # Extract data from frontend
        question = data.get('question', '')
        language = data.get('language', 'en-US')
        context = data.get('context', {})
        
        print(f"Server received question: {question}")
        print(f"Language: {language}")
        print(f"Context: {context}")
        
        # Enhanced prompt based on language and context
        if language == 'ml-IN':
            # Malayalam-specific prompt
            prompt_template = """
            നിങ്ങൾ കേരളത്തിലെ കർഷകർക്കുള്ള ഒരു വിദഗ്ധ കാർഷിക സഹായിയാണ്. താഴെയുള്ള സന്ദർഭത്തെ ഉപയോഗിച്ച് ഉപയോക്താവിന്റെ ചോദ്യത്തിന് ഉത്തരം നൽകുക.
            സന്ദർഭത്തിൽ നിന്ന് ഉത്തരം അറിയില്ലെങ്കിൽ, മതിയായ വിവരങ്ങൾ ഇല്ലെന്ന് പറയുക, ഉത്തരം കണ്ടുപിടിക്കാൻ ശ്രമിക്കരുത്.
            വ്യക്തവും ലളിതവും സഹായകരവുമായ രീതിയിൽ ഉത്തരം നൽകുക.

            സന്ദർഭം: {context}

            ചോദ്യം: {question}

            സഹായകരമായ ഉത്തരം:
            """
        else:
            # English prompt
            prompt_template = """
            You are an expert agricultural assistant for farmers in Kerala, India. Use the following pieces of context to answer the user's question.
            If you don't know the answer from the context, just say that you don't have enough information, don't try to make up an answer.
            Answer in a clear, simple, and helpful way.

            CONTEXT: {context}

            QUESTION: {question}

            HELPFUL ANSWER:
            """
        
        # Get AI response
        if qa_chain:
            response = qa_chain.invoke({"query": question})
            response_text = response['result']
        else:
            response_text = "AI chain is not ready. Please wait a moment and try again."
        
        # Calculate response time
        response_time = 1.23  # You can add actual timing if needed
        
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

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_ready': qa_chain is not None
    })

# Voice-specific endpoint (for future enhancement)
@app.route('/api/voice', methods=['POST'])
def process_voice():
    data = request.get_json()
    transcript = data.get('transcript', '')
    language = data.get('language', 'en-US')
    
    # Process voice input the same way as text
    return ask_question()

# Image analysis endpoint (for future enhancement)
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
    print("📚 Loading AI knowledge base...")
    
    # Reload the vector store from disk
    vector_store_from_disk = Chroma(persist_directory="db", embedding_function=embeddings)
    
    # Create a retriever
    retriever = vector_store_from_disk.as_retriever(search_kwargs={"k": 2})

    # Create the prompt template
    prompt_template = """
    You are an expert agricultural assistant for farmers in Kerala, India. Use the following pieces of context to answer the user's question.
    If you don't know the answer from the context, just say that you don't have enough information, don't try to make up an answer.
    Answer in a clear, simple, and helpful way.

    CONTEXT: {context}

    QUESTION: {question}

    HELPFUL ANSWER:
    """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    # Create the final QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    print("✅ AI system ready!")
    print("🌐 Server starting on http://127.0.0.1:5000")
    print("📱 Frontend can now connect to this backend")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
