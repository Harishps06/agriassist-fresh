#!/usr/bin/env python3
"""
Agricultural Document Processor – Clean Architecture
Handles:
  - PDF + TXT text extraction
  - Text cleaning & classification into sections
  - Configurable keywords from JSON
  - Knowledge base saving/loading/searching with advanced relevance ranking
"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Union
import json
import logging
import re

# Primary extraction libraries
import fitz  # PyMuPDF
import PyPDF2  # Fallback if fitz fails

# -----------------------------
# Logging setup
# -----------------------------
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class AgriculturalDocumentProcessor:
    def __init__(self,
                 knowledge_base_dir: str = "knowledge_base",
                 keyword_config_file: str = "keywords_config.json"):
        """
        :param knowledge_base_dir: directory to store JSON knowledge files
        :param keyword_config_file: path to JSON config of keywords
        """
        self.knowledge_base_dir = Path(knowledge_base_dir)
        self.knowledge_base_dir.mkdir(exist_ok=True)
        self.keyword_config_file = Path(keyword_config_file)
        self.section_keywords = self._load_keywords()
        self.processed_files: List[str] = []

    # ---------- CONFIG LOADING ----------
    def _load_keywords(self) -> Dict[str, List[str]]:
        """Load section keywords from JSON config"""
        if self.keyword_config_file.exists():
            try:
                with open(self.keyword_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading keyword config {self.keyword_config_file}: {e}")
        logger.warning("Keyword config missing or unreadable. Using default minimal sections.")
        return {
            'general': ['advice', 'guidance', 'tip', 'information']
        }

    # ---------- FILE TYPE HANDLING ----------
    def _is_pdf(self, path: str) -> bool:
        return Path(path).suffix.lower() == '.pdf'

    def _is_txt(self, path: str) -> bool:
        return Path(path).suffix.lower() == '.txt'

    # ---------- TEXT EXTRACTION ----------
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using PyMuPDF first, then PyPDF2 as fallback"""
        try:
            with fitz.open(pdf_path) as doc:
                text = "\n".join(page.get_text() for page in doc)
            return text.strip()
        except Exception as e:
            logger.warning(f"PyMuPDF failed for {pdf_path}: {e}")

        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = "\n".join(page.extract_text() or '' for page in reader.pages)
            return text.strip()
        except Exception as e:
            logger.error(f"Both extraction methods failed for {pdf_path}: {e}")
            return ""

    def extract_text_from_txt(self, txt_path: str) -> str:
        """Extract text from a .txt file"""
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text.strip()
        except Exception as e:
            logger.error(f"Error reading TXT file {txt_path}: {e}")
            return ""

    # ---------- CLEAN TEXT ----------
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'[^\w\s\u0D00-\u0D7F.,!?;:/%+\-]', ' ', text)
        return text.strip()

    # ---------- CLASSIFY SECTIONS ----------
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Classify text sentences into agricultural sections"""
        sections = {k: '' for k in self.section_keywords.keys()}
        sentences = re.split(r'[.!?]+', text)

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 8:
                continue
            for section, keywords in self.section_keywords.items():
                for kw in keywords:
                    if re.search(r'\b' + re.escape(kw.lower()) + r'\b', sentence.lower()):
                        sections[section] += sentence + ". "
                        break
        return sections

    # ---------- PROCESS FILE ----------
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Extract, clean, classify one file (PDF or TXT)"""
        logger.info(f"Processing file: {file_path}")
        if self._is_pdf(file_path):
            raw_text = self.extract_text_from_pdf(file_path)
        elif self._is_txt(file_path):
            raw_text = self.extract_text_from_txt(file_path)
        else:
            return {"error": f"Unsupported file type: {file_path}"}

        if not raw_text:
            return {"error": "Could not extract text"}

        cleaned_text = self.clean_text(raw_text)
        sections = self.extract_sections(cleaned_text)

        processed_at = datetime.fromtimestamp(Path(file_path).stat().st_mtime).isoformat()

        knowledge_entry = {
            'file_name': Path(file_path).name,
            'file_path': file_path,
            'processed_at': processed_at,
            'total_text_length': len(cleaned_text),
            'sections': sections,
            'full_text': cleaned_text[:5000]
        }
        return knowledge_entry

    # ---------- SAVE ----------
    def save_entry(self, knowledge_entry: Dict[str, Any]) -> str:
        """Save processed knowledge entry as JSON"""
        filename = f"{Path(knowledge_entry['file_name']).stem}_knowledge.json"
        filepath = self.knowledge_base_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(knowledge_entry, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved knowledge entry: {filepath}")
        return str(filepath)

    # ---------- PROCESS MULTIPLE ----------
    def process_multiple_files(self, directory: str) -> List[Dict[str, Any]]:
        """Process all PDFs and TXTs in a directory"""
        dir_path = Path(directory)
        if not dir_path.exists():
            logger.error(f"Directory not found: {directory}")
            return []
        files = list(dir_path.glob("*.pdf")) + list(dir_path.glob("*.txt"))
        if not files:
            logger.warning(f"No PDF/TXT files found in {directory}")
            return []

        processed_entries = []
        for file in files:
            try:
                entry = self.process_file(str(file))
                if 'error' not in entry:
                    saved_path = self.save_entry(entry)
                    entry['saved_path'] = saved_path
                    processed_entries.append(entry)
                    self.processed_files.append(str(file))
                else:
                    logger.error(f"Failed to process {file}: {entry['error']}")
            except Exception as e:
                logger.error(f"Error processing {file}: {e}")
        return processed_entries

    # ---------- LOAD KNOWLEDGE ----------
    def load_all_knowledge(self) -> Dict[str, Any]:
        """Load all processed knowledge JSON files"""
        knowledge_base = {k: [] for k in self.section_keywords.keys()}
        json_files = list(self.knowledge_base_dir.glob("*_knowledge.json"))

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for section, content in data.get('sections', {}).items():
                    if content.strip() and section in knowledge_base:
                        knowledge_base[section].append({
                            'source': data['file_name'],
                            'content': content.strip()
                        })
            except Exception as e:
                logger.error(f"Error loading {json_file}: {e}")

        return knowledge_base

    # ---------- ADVANCED SEARCH ----------
    def search_knowledge(self,
                         query: str,
                         knowledge_base: Dict[str, Any],
                         min_score: float = 0.1) -> List[Dict[str, str]]:
        """
        Search knowledge base using ranked relevance:
          - Token overlap
          - Keyword match
          - Partial/phrase match
        """
        query_lower = query.lower()
        query_tokens = set(query_lower.split())
        results = []

        for section, entries in knowledge_base.items():
            for entry in entries:
                content_lower = entry['content'].lower()

                # Exact phrase match gets bonus
                phrase_score = 2.0 if query_lower in content_lower else 0.0

                # Token overlap score
                entry_tokens = set(content_lower.split())
                overlap = len(query_tokens & entry_tokens)
                overlap_score = overlap / max(len(query_tokens), 1)

                # Partial match
                partial_score = 1.0 if any(q in content_lower for q in query_tokens) else 0.0

                total_score = phrase_score + overlap_score + partial_score

                if total_score >= min_score:
                    results.append({
                        'section': section,
                        'source': entry['source'],
                        'score': round(total_score, 3),
                        'content': entry['content'][:500] + "..." if len(entry['content']) > 500 else entry['content']
                    })

        # Sort results by score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        return results


# -----------------------------
# Backward compatibility aliases
# -----------------------------
AgriculturalPDFProcessor = AgriculturalDocumentProcessor

def main():
    """Example usage"""
    processor = AgriculturalDocumentProcessor()
    
    # Process files
    processed_entries = processor.process_multiple_files("agricultural_pdfs")
    print(f"Processed {len(processed_entries)} files")
    
    # Load knowledge
    knowledge_base = processor.load_all_knowledge()
    total_entries = sum(len(entries) for entries in knowledge_base.values())
    print(f"Loaded {total_entries} knowledge entries")
    
    # Search
    results = processor.search_knowledge("coconut cultivation", knowledge_base)
    print(f"Found {len(results)} relevant entries")
    for result in results[:3]:
        print(f"Score: {result['score']} | Section: {result['section']} | Source: {result['source']}")

if __name__ == "__main__":
    main()