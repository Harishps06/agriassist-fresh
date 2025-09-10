# 🌾 AgriAssist PDF Knowledge Base Setup

This guide helps you add your agricultural PDFs to improve your website's responses.

## 🚀 Quick Start (5 minutes)

### Step 1: Prepare Your PDFs
```bash
# Create a folder for your PDFs
mkdir agricultural_pdfs

# Copy your agricultural PDFs here
cp /path/to/your/*.pdf agricultural_pdfs/
```

### Step 2: Run Quick Setup
```bash
cd backend
python quick_setup.py
```

### Step 3: Process Your PDFs
```bash
python setup_pdf_knowledge.py
```

### Step 4: Deploy Enhanced Backend
```bash
# Use the PDF-enhanced version
mv app_with_pdf.py app.py

# Deploy to Render (your existing deployment)
```

## 📁 File Structure

```
backend/
├── agricultural_pdfs/          # ← Put your PDFs here
│   ├── rice_cultivation.pdf
│   ├── coconut_farming.pdf
│   ├── pest_control.pdf
│   └── soil_management.pdf
├── knowledge_base/             # ← Generated knowledge base
│   ├── rice_cultivation_knowledge.json
│   ├── coconut_farming_knowledge.json
│   └── summary.json
├── app_with_pdf.py            # ← Enhanced backend
├── pdf_processor.py           # ← PDF processing logic
├── setup_pdf_knowledge.py     # ← PDF setup script
└── quick_setup.py             # ← Quick setup script
```

## 🔧 How It Works

1. **PDF Processing**: Extracts text from your agricultural PDFs
2. **Smart Organization**: Automatically categorizes content by topics
3. **Knowledge Base**: Creates searchable knowledge entries
4. **Enhanced Responses**: Uses PDF content to answer questions better

## 📊 Supported Topics

- 🌾 Crop cultivation (rice, coconut, vegetables)
- 🐛 Pest and disease control
- 🌱 Fertilizer management
- 💧 Irrigation techniques
- 🌾 Harvesting methods
- 🌍 Soil management
- 🌤️ Weather guidance
- 💰 Market information
- 📚 General agricultural advice

## 🎯 Benefits

- **Better Responses**: More accurate and detailed answers
- **Your Knowledge**: Uses your specific agricultural documents
- **Bilingual Support**: Works with Malayalam and English PDFs
- **Source Attribution**: Shows which PDF provided the information
- **Scalable**: Add more PDFs anytime to improve responses

## 🚨 Important Notes

- **PDF Quality**: Use PDFs with clear, readable text
- **File Size**: Large PDFs are supported but may take longer to process
- **Language**: Both Malayalam and English PDFs work
- **Topics**: Focus on agricultural content for best results

## 🔍 Testing

After setup, test your enhanced backend:

```bash
# Check knowledge base stats
curl https://your-backend-url.onrender.com/api/knowledge-stats

# Test with a question
curl -X POST https://your-backend-url.onrender.com/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How to grow rice?", "language": "en-US"}'
```

## 🆘 Troubleshooting

### PDF Processing Issues
- Check PDF is readable (not scanned images)
- Ensure PDF has text content
- Try with smaller PDFs first

### Knowledge Base Issues
- Check `knowledge_base/` folder for generated files
- Verify PDFs were processed successfully
- Check backend logs for errors

### Memory Issues
- Split large PDFs into smaller files
- Process PDFs in batches
- Use text-only PDFs when possible

## 📞 Support

If you need help:
1. Check the logs in your Render dashboard
2. Verify PDF processing worked
3. Test the knowledge base stats endpoint
4. Check the generated JSON files in `knowledge_base/`

Your enhanced AgriAssist will now provide much better agricultural advice using your PDF knowledge base! 🌾✨
