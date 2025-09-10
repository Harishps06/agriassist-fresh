# Deploy AgriAssist with PDF Knowledge Base

This guide helps you deploy the enhanced AgriAssist backend that can process and use agricultural PDFs to provide better responses.

## 🚀 Quick Start

### 1. Prepare Your PDFs

1. **Create a folder** for your agricultural PDFs:
   ```bash
   mkdir agricultural_pdfs
   ```

2. **Copy your PDFs** into this folder:
   ```bash
   cp /path/to/your/*.pdf agricultural_pdfs/
   ```

3. **Organize by topic** (optional but recommended):
   ```
   agricultural_pdfs/
   ├── rice_cultivation.pdf
   ├── coconut_farming.pdf
   ├── pest_control.pdf
   ├── soil_management.pdf
   └── weather_guidance.pdf
   ```

### 2. Process PDFs Locally

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run the PDF processor**:
   ```bash
   python setup_pdf_knowledge.py
   ```

3. **Follow the prompts** to process your PDFs

### 3. Deploy to Render

1. **Update your backend** to use the PDF-enhanced version:
   ```bash
   # Rename the current app
   mv app_simple.py app_simple_backup.py
   
   # Use the PDF-enhanced version
   mv app_with_pdf.py app.py
   ```

2. **Deploy to Render**:
   - Go to your Render dashboard
   - Redeploy your service
   - The new backend will automatically load the knowledge base

### 4. Test the Enhanced Backend

1. **Check knowledge base stats**:
   ```bash
   curl https://your-backend-url.onrender.com/api/knowledge-stats
   ```

2. **Test with agricultural questions**:
   ```bash
   curl -X POST https://your-backend-url.onrender.com/api/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "How to control rice pests?", "language": "en-US"}'
   ```

## 📊 Features

### PDF Processing
- **Automatic text extraction** from PDFs
- **Smart section detection** (cultivation, pests, fertilizers, etc.)
- **Malayalam and English support**
- **Knowledge organization** by agricultural topics

### Enhanced Responses
- **PDF-based answers** using your agricultural documents
- **Source attribution** showing which PDF provided the information
- **Fallback responses** if PDF knowledge is not available
- **Bilingual support** (Malayalam/English)

### API Endpoints

#### Process PDFs
```bash
POST /api/process-pdfs
{
  "pdf_directory": "agricultural_pdfs"
}
```

#### Get Knowledge Stats
```bash
GET /api/knowledge-stats
```

#### Ask Questions (Enhanced)
```bash
POST /api/ask
{
  "question": "How to grow rice?",
  "language": "en-US"
}
```

## 🔧 Configuration

### Environment Variables
```bash
GOOGLE_API_KEY=your_gemini_api_key
```

### File Structure
```
backend/
├── app.py                    # Main application
├── pdf_processor.py         # PDF processing logic
├── setup_pdf_knowledge.py   # PDF setup script
├── requirements.txt         # Dependencies
├── knowledge_base/          # Processed knowledge
│   ├── rice_cultivation_knowledge.json
│   ├── coconut_farming_knowledge.json
│   └── summary.json
└── agricultural_pdfs/       # Your PDF files
    ├── rice_guide.pdf
    ├── coconut_manual.pdf
    └── pest_control.pdf
```

## 📈 Performance Tips

### For Large PDFs
1. **Split large PDFs** into smaller, topic-specific files
2. **Use descriptive filenames** (e.g., `rice_cultivation.pdf`)
3. **Process in batches** if you have many PDFs

### For Better Results
1. **Use high-quality PDFs** with clear text
2. **Include both Malayalam and English** content
3. **Organize by agricultural topics**

## 🐛 Troubleshooting

### PDF Processing Issues
```bash
# Check if PDFs are readable
python -c "import fitz; print('PyMuPDF working')"

# Test PDF processing
python pdf_processor.py
```

### Knowledge Base Issues
```bash
# Check knowledge base stats
curl https://your-backend-url.onrender.com/api/knowledge-stats

# Reload knowledge base
curl -X POST https://your-backend-url.onrender.com/api/process-pdfs
```

### Memory Issues
- **Reduce PDF size** by splitting large files
- **Process fewer PDFs** at once
- **Use text-only PDFs** when possible

## 📚 Example Usage

### Processing PDFs
```python
from pdf_processor import AgriculturalPDFProcessor

processor = AgriculturalPDFProcessor()
processed = processor.process_multiple_pdfs("agricultural_pdfs")
print(f"Processed {len(processed)} PDFs")
```

### Searching Knowledge
```python
knowledge_base = processor.load_all_knowledge()
results = processor.search_knowledge("rice cultivation", knowledge_base)
for result in results:
    print(f"Section: {result['section']}")
    print(f"Content: {result['content']}")
```

## 🎯 Next Steps

1. **Add more PDFs** to expand your knowledge base
2. **Test different questions** to see improved responses
3. **Monitor performance** and optimize as needed
4. **Consider adding** more agricultural topics

## 📞 Support

If you encounter issues:
1. Check the logs in Render dashboard
2. Test the health endpoint: `/api/health`
3. Verify PDF processing: `/api/knowledge-stats`
4. Check knowledge base files in `knowledge_base/` folder

Your enhanced AgriAssist backend is now ready to provide much better agricultural advice using your PDF knowledge base! 🌾
