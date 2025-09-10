#!/usr/bin/env python3
"""
Example usage of the PDF processor for AgriAssist
"""

from pdf_processor import AgriculturalPDFProcessor
import json

def main():
    print("🌾 AgriAssist PDF Processor - Example Usage")
    print("=" * 50)
    
    # Initialize the processor
    processor = AgriculturalPDFProcessor("knowledge_base")
    
    # Example 1: Process a single PDF
    print("\n📄 Example 1: Processing a single PDF")
    print("   (Replace 'example.pdf' with your actual PDF path)")
    
    # Uncomment the following lines when you have a PDF:
    # pdf_path = "agricultural_pdfs/example.pdf"
    # if Path(pdf_path).exists():
    #     knowledge_entry = processor.process_pdf(pdf_path)
    #     print(f"   Processed: {knowledge_entry['file_name']}")
    #     print(f"   Text length: {knowledge_entry['total_text_length']} characters")
    #     print(f"   Sections found: {len([s for s in knowledge_entry['sections'].values() if s])}")
    
    # Example 2: Process multiple PDFs
    print("\n📁 Example 2: Processing multiple PDFs")
    print("   (Put your PDFs in 'agricultural_pdfs' folder)")
    
    # Check if PDFs exist
    from pathlib import Path
    pdf_dir = Path("agricultural_pdfs")
    if pdf_dir.exists():
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if pdf_files:
            print(f"   Found {len(pdf_files)} PDF files:")
            for pdf in pdf_files:
                print(f"     - {pdf.name}")
            
            # Process them
            processed_entries = processor.process_multiple_pdfs("agricultural_pdfs")
            print(f"   Successfully processed {len(processed_entries)} PDFs")
            
            # Show knowledge base stats
            knowledge_base = processor.load_all_knowledge()
            print(f"\n📊 Knowledge Base Statistics:")
            total_entries = 0
            for section, entries in knowledge_base.items():
                if entries:
                    print(f"     {section}: {len(entries)} entries")
                    total_entries += len(entries)
            print(f"     Total entries: {total_entries}")
            
        else:
            print("   No PDF files found in 'agricultural_pdfs' folder")
            print("   Please add your agricultural PDFs there")
    else:
        print("   'agricultural_pdfs' folder not found")
        print("   Please create it and add your PDFs")
    
    # Example 3: Search knowledge
    print("\n🔍 Example 3: Searching knowledge base")
    if 'knowledge_base' in locals() and knowledge_base:
        query = "rice cultivation"
        results = processor.search_knowledge(query, knowledge_base)
        print(f"   Query: '{query}'")
        print(f"   Found {len(results)} relevant entries")
        
        for i, result in enumerate(results[:2], 1):  # Show first 2 results
            print(f"     {i}. Section: {result['section']}")
            print(f"        Source: {result['source']}")
            print(f"        Content: {result['content'][:100]}...")
    else:
        print("   No knowledge base available yet")
        print("   Process some PDFs first")
    
    # Example 4: Show how to use in your backend
    print("\n🚀 Example 4: Using in your backend")
    print("   To use this in your backend, replace your current app.py with app_with_pdf.py")
    print("   The enhanced backend will automatically:")
    print("     - Load the knowledge base on startup")
    print("     - Search PDF content for better responses")
    print("     - Provide source attribution")
    print("     - Fall back to simple responses if needed")
    
    print("\n✨ Next Steps:")
    print("1. Add your agricultural PDFs to 'agricultural_pdfs' folder")
    print("2. Run: python setup_pdf_knowledge.py")
    print("3. Deploy: python app_with_pdf.py")
    print("4. Test your enhanced knowledge base!")

if __name__ == "__main__":
    main()
