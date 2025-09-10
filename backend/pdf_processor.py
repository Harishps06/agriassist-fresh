import os
import PyPDF2
import fitz  # PyMuPDF
from pathlib import Path
import json
import re
from typing import List, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgriculturalPDFProcessor:
    def __init__(self, knowledge_base_dir: str = "knowledge_base"):
        self.knowledge_base_dir = Path(knowledge_base_dir)
        self.knowledge_base_dir.mkdir(exist_ok=True)
        self.processed_files = []
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using PyMuPDF for better accuracy"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
                text += "\n"  # Add page break
            
            doc.close()
            return text
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess extracted text"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        
        # Remove page numbers and headers/footers
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
        
        # Remove special characters but keep Malayalam and English
        text = re.sub(r'[^\w\s\u0D00-\u0D7F.,!?;:()\-]', ' ', text)
        
        return text.strip()
    
    def extract_agricultural_sections(self, text: str) -> Dict[str, str]:
        """Extract specific agricultural sections from text"""
        sections = {
            'crop_cultivation': '',
            'pest_diseases': '',
            'fertilizer_management': '',
            'irrigation': '',
            'harvesting': '',
            'soil_management': '',
            'weather_guidance': '',
            'market_information': '',
            'general_advice': ''
        }
        
        # Keywords for different sections
        keywords = {
            'crop_cultivation': ['cultivation', 'planting', 'sowing', 'കൃഷി', 'നടുക', 'വിത്ത്', 'വളരുക'],
            'pest_diseases': ['pest', 'disease', 'insect', 'രോഗം', 'കീടം', 'പ്രതിരോധം', 'നിയന്ത്രണം'],
            'fertilizer_management': ['fertilizer', 'manure', 'nutrient', 'വളം', 'ഊർജ്ജം', 'ഭക്ഷണം'],
            'irrigation': ['irrigation', 'watering', 'water', 'ജലസേചനം', 'വെള്ളം', 'ജലം'],
            'harvesting': ['harvest', 'yield', 'collection', 'വിളവെടുക്കുക', 'വിളവ്', 'ശേഖരണം'],
            'soil_management': ['soil', 'land', 'മണ്ണ്', 'ഭൂമി', 'ഭൂമിശാസ്ത്രം'],
            'weather_guidance': ['weather', 'climate', 'rain', 'കാലാവസ്ഥ', 'മഴ', 'താപനില'],
            'market_information': ['market', 'price', 'selling', 'വിപണി', 'വില', 'വിൽപ്പന'],
            'general_advice': ['advice', 'tips', 'guidance', 'ഉപദേശം', 'സഹായം', 'മാർഗദർശനം']
        }
        
        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Skip very short sentences
                continue
                
            for section, section_keywords in keywords.items():
                if any(keyword.lower() in sentence.lower() for keyword in section_keywords):
                    sections[section] += sentence + ". "
        
        return sections
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Process a single PDF file and extract agricultural knowledge"""
        logger.info(f"Processing PDF: {pdf_path}")
        
        # Extract text
        raw_text = self.extract_text_from_pdf(pdf_path)
        if not raw_text:
            return {"error": "Could not extract text from PDF"}
        
        # Clean text
        cleaned_text = self.clean_text(raw_text)
        
        # Extract sections
        sections = self.extract_agricultural_sections(cleaned_text)
        
        # Create knowledge entry
        knowledge_entry = {
            'file_name': Path(pdf_path).name,
            'file_path': pdf_path,
            'processed_at': str(Path(pdf_path).stat().st_mtime),
            'total_text_length': len(cleaned_text),
            'sections': sections,
            'full_text': cleaned_text[:5000]  # Store first 5000 chars for reference
        }
        
        return knowledge_entry
    
    def save_knowledge_entry(self, knowledge_entry: Dict[str, Any]) -> str:
        """Save processed knowledge to JSON file"""
        filename = f"{Path(knowledge_entry['file_name']).stem}_knowledge.json"
        filepath = self.knowledge_base_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(knowledge_entry, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved knowledge entry: {filepath}")
        return str(filepath)
    
    def process_multiple_pdfs(self, pdf_directory: str) -> List[Dict[str, Any]]:
        """Process all PDFs in a directory"""
        pdf_dir = Path(pdf_directory)
        if not pdf_dir.exists():
            logger.error(f"Directory not found: {pdf_directory}")
            return []
        
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {pdf_directory}")
            return []
        
        processed_entries = []
        
        for pdf_file in pdf_files:
            try:
                knowledge_entry = self.process_pdf(str(pdf_file))
                if 'error' not in knowledge_entry:
                    saved_path = self.save_knowledge_entry(knowledge_entry)
                    knowledge_entry['saved_path'] = saved_path
                    processed_entries.append(knowledge_entry)
                    self.processed_files.append(str(pdf_file))
                else:
                    logger.error(f"Failed to process {pdf_file}: {knowledge_entry['error']}")
            except Exception as e:
                logger.error(f"Error processing {pdf_file}: {str(e)}")
        
        return processed_entries
    
    def load_all_knowledge(self) -> Dict[str, Any]:
        """Load all processed knowledge from JSON files"""
        knowledge_base = {
            'crop_cultivation': [],
            'pest_diseases': [],
            'fertilizer_management': [],
            'irrigation': [],
            'harvesting': [],
            'soil_management': [],
            'weather_guidance': [],
            'market_information': [],
            'general_advice': []
        }
        
        json_files = list(self.knowledge_base_dir.glob("*_knowledge.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Add sections to knowledge base
                for section, content in data.get('sections', {}).items():
                    if content.strip() and section in knowledge_base:
                        knowledge_base[section].append({
                            'source': data['file_name'],
                            'content': content.strip()
                        })
            except Exception as e:
                logger.error(f"Error loading {json_file}: {str(e)}")
        
        return knowledge_base
    
    def search_knowledge(self, query: str, knowledge_base: Dict[str, Any]) -> List[Dict[str, str]]:
        """Search through knowledge base for relevant information"""
        query_lower = query.lower()
        results = []
        
        for section, entries in knowledge_base.items():
            for entry in entries:
                content_lower = entry['content'].lower()
                if any(word in content_lower for word in query_lower.split()):
                    results.append({
                        'section': section,
                        'source': entry['source'],
                        'content': entry['content'][:500] + "..." if len(entry['content']) > 500 else entry['content']
                    })
        
        return results

def main():
    """Example usage of the PDF processor"""
    processor = AgriculturalPDFProcessor()
    
    # Process PDFs from a directory
    pdf_directory = "agricultural_pdfs"  # Change this to your PDF directory
    processed_entries = processor.process_multiple_pdfs(pdf_directory)
    
    print(f"Processed {len(processed_entries)} PDF files")
    
    # Load all knowledge
    knowledge_base = processor.load_all_knowledge()
    
    # Example search
    query = "rice cultivation"
    results = processor.search_knowledge(query, knowledge_base)
    
    print(f"Found {len(results)} relevant entries for '{query}'")
    for result in results[:3]:  # Show first 3 results
        print(f"Section: {result['section']}")
        print(f"Source: {result['source']}")
        print(f"Content: {result['content'][:200]}...")
        print("-" * 50)

if __name__ == "__main__":
    main()
