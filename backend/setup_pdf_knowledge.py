#!/usr/bin/env python3
"""
Setup script for processing agricultural PDFs and building knowledge base
"""

import os
import sys
from pathlib import Path
from pdf_processor import AgriculturalPDFProcessor
import json

def main():
    print("🌾 AgriAssist PDF Knowledge Base Setup")
    print("=" * 50)
    
    # Initialize PDF processor
    processor = AgriculturalPDFProcessor("knowledge_base")
    
    # Get PDF directory from user
    print("\n📁 Please provide the path to your agricultural PDFs:")
    print("   (You can put all your PDFs in a folder and provide the path)")
    
    pdf_directory = input("PDF Directory Path: ").strip()
    
    if not pdf_directory:
        print("❌ No directory provided. Exiting.")
        return
    
    pdf_path = Path(pdf_directory)
    if not pdf_path.exists():
        print(f"❌ Directory not found: {pdf_directory}")
        return
    
    if not pdf_path.is_dir():
        print(f"❌ Path is not a directory: {pdf_directory}")
        return
    
    # Check for PDF files
    pdf_files = list(pdf_path.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ No PDF files found in {pdf_directory}")
        return
    
    print(f"\n📄 Found {len(pdf_files)} PDF files:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"   {i}. {pdf_file.name}")
    
    # Confirm processing
    print(f"\n🔄 Ready to process {len(pdf_files)} PDF files...")
    confirm = input("Continue? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Processing cancelled.")
        return
    
    # Process PDFs
    print("\n🔄 Processing PDFs...")
    try:
        processed_entries = processor.process_multiple_pdfs(pdf_directory)
        
        if processed_entries:
            print(f"\n✅ Successfully processed {len(processed_entries)} PDF files!")
            
            # Show summary
            print("\n📊 Knowledge Base Summary:")
            knowledge_base = processor.load_all_knowledge()
            
            total_entries = 0
            for section, entries in knowledge_base.items():
                if entries:
                    print(f"   {section}: {len(entries)} entries")
                    total_entries += len(entries)
            
            print(f"\n📈 Total knowledge entries: {total_entries}")
            
            # Save summary
            summary = {
                'processed_files': len(processed_entries),
                'total_entries': total_entries,
                'sections': {k: len(v) for k, v in knowledge_base.items() if v},
                'files': [entry['file_name'] for entry in processed_entries]
            }
            
            with open('knowledge_base/summary.json', 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 Summary saved to: knowledge_base/summary.json")
            print(f"\n🚀 Your knowledge base is ready!")
            print(f"   You can now start the enhanced backend with: python app_with_pdf.py")
            
        else:
            print("❌ No PDFs were successfully processed.")
            
    except Exception as e:
        print(f"❌ Error processing PDFs: {str(e)}")
        return

def show_help():
    print("🌾 AgriAssist PDF Knowledge Base Setup")
    print("=" * 50)
    print("\nThis script helps you process agricultural PDFs and build a knowledge base.")
    print("\nSteps:")
    print("1. Put all your agricultural PDFs in a folder")
    print("2. Run this script and provide the folder path")
    print("3. The script will extract text and organize it by topics")
    print("4. Start the enhanced backend to use the knowledge base")
    print("\nExample:")
    print("   python setup_pdf_knowledge.py")
    print("\nSupported PDF topics:")
    print("   - Crop cultivation")
    print("   - Pest and disease control")
    print("   - Fertilizer management")
    print("   - Irrigation")
    print("   - Harvesting")
    print("   - Soil management")
    print("   - Weather guidance")
    print("   - Market information")
    print("   - General agricultural advice")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
    else:
        main()
