# Backend Integration Guide for AgriAssist

## 🔗 Backend Server Requirements

Your backend server needs to handle the enhanced request format from the frontend. Here's what you need to implement:

### 1. Enhanced API Endpoint

**Endpoint:** `POST /api/ask`

**Request Format:**
```json
{
  "question": "What's wrong with my rice?",
  "language": "en-US",
  "context": {
    "timestamp": "2025-01-27T10:30:00Z",
    "userAgent": "Mozilla/5.0...",
    "location": "Kerala, India",
    "sessionId": "session_1234567890_abc123"
  }
}
```

**Response Format:**
```json
{
  "answer": "Your AI response here...",
  "responseTime": 1.23,
  "sources": ["source1", "source2"],
  "confidence": 0.95,
  "language": "en-US"
}
```

### 2. CORS Configuration

Enable CORS for your frontend domain:

```python
# Flask example
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",
    "https://your-frontend-domain.com",
    "https://your-username.github.io"
])
```

```javascript
// Express.js example
const cors = require('cors');

app.use(cors({
    origin: [
        'http://localhost:3000',
        'https://your-frontend-domain.com',
        'https://your-username.github.io'
    ],
    credentials: true
}));
```

### 3. Voice Recognition Integration

Your backend should handle voice-related queries:

```python
def process_voice_query(question, language, context):
    # Detect if it's a voice query
    if context.get('inputType') == 'voice':
        # Process with voice-specific logic
        pass
    
    # Handle language-specific processing
    if language == 'ml-IN':
        # Malayalam-specific processing
        pass
    elif language == 'en-US':
        # English-specific processing
        pass
```

### 4. Image Analysis Integration

For image analysis, your backend can:

```python
def process_image_analysis(image_data, additional_prompt):
    # Forward to Gemini Vision API
    # Process agricultural-specific analysis
    # Return structured response
    pass
```

## 🚀 Quick Backend Setup

### Option 1: Python Flask Backend

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    
    question = data.get('question')
    language = data.get('language', 'en-US')
    context = data.get('context', {})
    
    # Your AI processing logic here
    answer = process_question(question, language, context)
    
    return jsonify({
        'answer': answer,
        'responseTime': 1.23,
        'language': language
    })

def process_question(question, language, context):
    # Implement your RAG system here
    # This is where you'd integrate with your AI model
    return "This is a sample response from your backend"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Option 2: Node.js Express Backend

```javascript
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

app.post('/api/ask', async (req, res) => {
    const { question, language, context } = req.body;
    
    try {
        // Your AI processing logic here
        const answer = await processQuestion(question, language, context);
        
        res.json({
            answer: answer,
            responseTime: 1.23,
            language: language
        });
    } catch (error) {
        res.status(500).json({ error: 'Internal server error' });
    }
});

async function processQuestion(question, language, context) {
    // Implement your RAG system here
    return "This is a sample response from your backend";
}

app.listen(5000, () => {
    console.log('Backend server running on port 5000');
});
```

## 🔧 Environment Configuration

### Development
```bash
# Backend URL
http://127.0.0.1:5000

# Frontend URL
http://localhost:3000
```

### Production
```bash
# Backend URL
https://your-backend-domain.com

# Frontend URL
https://your-frontend-domain.com
```

## 📱 Mobile App Integration

If you plan to create a mobile app later, your backend should also support:

1. **Push Notifications** - For weather alerts, farming tips
2. **User Authentication** - For personalized experiences
3. **Data Synchronization** - For offline/online data sync
4. **File Upload** - For image analysis

## 🔍 Testing Your Backend

### Test with curl:
```bash
curl -X POST http://127.0.0.1:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the best time to plant rice?",
    "language": "en-US",
    "context": {
      "timestamp": "2025-01-27T10:30:00Z",
      "location": "Kerala, India"
    }
  }'
```

### Test with JavaScript:
```javascript
fetch('http://127.0.0.1:5000/api/ask', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        question: 'What is the best time to plant rice?',
        language: 'en-US',
        context: {
            timestamp: new Date().toISOString(),
            location: 'Kerala, India'
        }
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🚨 Important Notes

1. **HTTPS Required**: For production, use HTTPS for security
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **Error Handling**: Provide meaningful error messages
4. **Logging**: Log requests for debugging and analytics
5. **Validation**: Validate input data before processing

## 🔄 Next Steps

1. Set up your backend server
2. Update the frontend configuration with your backend URL
3. Test the integration
4. Deploy both frontend and backend
5. Monitor and optimize performance
