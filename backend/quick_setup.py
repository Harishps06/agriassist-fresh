#!/usr/bin/env python3
"""
Quick setup script for AgriAssist PDF Knowledge Base
"""

import os
import sys
from pathlib import Path

def main():
    print("🌾 AgriAssist PDF Knowledge Base - Quick Setup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        print("❌ Please run this script from the backend directory")
        print("   cd backend && python quick_setup.py")
        return
    
    print("\n📋 This script will help you set up PDF processing for your agricultural knowledge base.")
    print("\nWhat you need:")
    print("1. Agricultural PDFs (any size)")
    print("2. Python environment with required packages")
    print("3. About 5-10 minutes")
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    try:
        import PyPDF2
        import fitz
        print("✅ PDF processing libraries found")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Installing required packages...")
        os.system("pip install PyPDF2 PyMuPDF")
    
    # Create directories
    print("\n📁 Creating directories...")
    Path("knowledge_base").mkdir(exist_ok=True)
    Path("agricultural_pdfs").mkdir(exist_ok=True)
    print("✅ Directories created")
    
    # Check for existing PDFs
    pdf_dir = Path("agricultural_pdfs")
    existing_pdfs = list(pdf_dir.glob("*.pdf"))
    
    if existing_pdfs:
        print(f"\n📄 Found {len(existing_pdfs)} existing PDFs:")
        for pdf in existing_pdfs:
            print(f"   - {pdf.name}")
        
        process_existing = input("\n🔄 Process existing PDFs? (y/n): ").strip().lower()
        if process_existing == 'y':
            print("\n🔄 Processing existing PDFs...")
            os.system("python setup_pdf_knowledge.py")
    else:
        print("\n📁 No PDFs found in agricultural_pdfs/ folder")
        print("   Please add your agricultural PDFs to the 'agricultural_pdfs' folder")
        print("   Then run: python setup_pdf_knowledge.py")
    
    # Show next steps
    print("\n🚀 Next Steps:")
    print("1. Add your agricultural PDFs to 'agricultural_pdfs/' folder")
    print("2. Run: python setup_pdf_knowledge.py")
    print("3. Deploy the enhanced backend: python app_with_pdf.py")
    print("4. Test your enhanced knowledge base!")
    
    print("\n📚 Supported PDF topics:")
    topics = [
        "Crop cultivation (rice, coconut, vegetables)",
        "Pest and disease control",
        "Fertilizer management",
        "Irrigation techniques",
        "Harvesting methods",
        "Soil management",
        "Weather guidance",
        "Market information",
        "General agricultural advice"
    ]
    
    for topic in topics:
        print(f"   • {topic}")
    
    print("\n✨ Your enhanced AgriAssist backend will provide much better responses!")
    print("   The more PDFs you add, the better the responses will be.")

if __name__ == "__main__":
    main()
