#!/usr/bin/env python3
"""
Test script for the new AgriculturalDocumentProcessor
"""

import os
import json
import logging
import re
from typing import List, Dict, Any
from pathlib import Path
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

class AgriculturalDocumentProcessor:
    def __init__(self, knowledge_base_dir: str = "knowledge_base",
                 keyword_config_file: str = "keywords_config.json"):
        """
        Initialize processor with knowledge base folder & keyword config file.
        """
        self.knowledge_base_dir = knowledge_base_dir
        self.keyword_config_file = keyword_config_file

        # Load keyword configuration
        self.keywords_config = self._load_keyword_config()

    # ----------------------------------------------------------------------
    # Internal Helpers
    # ----------------------------------------------------------------------
    def _load_keyword_config(self) -> Dict[str, List[str]]:
        """
        Load JSON keyword configuration.
        """
        if not os.path.exists(self.keyword_config_file):
            logger.warning(f"Keyword config not found: {self.keyword_config_file}")
            return {}

        try:
            with open(self.keyword_config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"Loaded keyword configuration: {len(config)} keyword groups")
            return config
        except Exception as e:
            logger.error(f"Error loading keyword config: {str(e)}")
            return {}

    def _read_pdf(self, file_path: str) -> str:
        """
        Extract text from PDF file.
        """
        try:
            reader = PdfReader(file_path)
            text_content = []
            for page in reader.pages:
                txt = page.extract_text()
                if txt:
                    text_content.append(txt)
            return "\n".join(text_content)
        except Exception as e:
            logger.error(f"Error reading PDF {file_path}: {str(e)}")
            return ""

    def _read_txt(self, file_path: str) -> str:
        """
        Read text from a .txt file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading TXT {file_path}: {str(e)}")
            return ""

    # ----------------------------------------------------------------------
    # Public Methods
    # ----------------------------------------------------------------------
    def load_all_knowledge(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load all PDF and TXT files from the knowledge base directory.
        Returns:
            Dict[filename, List[{"content": str, "tags": List[str]}]]
        """
        knowledge_data = {}
        base_path = Path(self.knowledge_base_dir)

        if not base_path.exists():
            logger.warning(f"Knowledge base directory does not exist: {base_path}")
            return {}

        for file_path in base_path.rglob("*"):
            if file_path.is_file():
                content = ""
                if file_path.suffix.lower() == ".pdf":
                    content = self._read_pdf(str(file_path))
                elif file_path.suffix.lower() == ".txt":
                    content = self._read_txt(str(file_path))

                if content:
                    tags = self._extract_tags(content)
                    knowledge_data.setdefault(file_path.name, []).append({
                        "content": content,
                        "tags": tags
                    })

        logger.info(f"Loaded knowledge base: {len(knowledge_data)} files")
        return knowledge_data

    def _extract_tags(self, text: str) -> List[str]:
        """
        Extract tags from content using keywords_config.
        """
        found_tags = set()
        for group, keywords in self.keywords_config.items():
            for kw in keywords:
                if re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE):
                    found_tags.add(group)
        return list(found_tags)

    def search_knowledge(self, query: str,
                         knowledge_base: Dict[str, List[Dict[str, Any]]],
                         top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Advanced search across the knowledge base.
        Scoring:
            +2 if keyword tag matches
            +1 per query term match in content
        Returns top_k results sorted by score.
        """
        results = []
        query_terms = [q.lower() for q in re.findall(r"\w+", query)]

        for filename, entries in knowledge_base.items():
            for entry in entries:
                content = entry.get("content", "")
                tags = entry.get("tags", [])
                score = 0

                # Tag match
                for t in tags:
                    if any(q in t.lower() for q in query_terms):
                        score += 2

                # Content match
                for term in query_terms:
                    score += content.lower().count(term)

                if score > 0:
                    results.append({
                        "filename": filename,
                        "tags": tags,
                        "score": score,
                        "snippet": content[:300],
                        "content": content
                    })

        results = sorted(results, key=lambda x: x["score"], reverse=True)
        return results[:top_k]


# ----------------------------------------------------------------------
# Test the processor
# ----------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🧪 TESTING NEW AGRICULTURAL DOCUMENT PROCESSOR")
    print("=" * 50)
    
    processor = AgriculturalDocumentProcessor(
        knowledge_base_dir="knowledge_base",
        keyword_config_file="keywords_config.json"
    )
    
    print("\n📚 Loading knowledge base...")
    kb = processor.load_all_knowledge()
    print(f"✅ Knowledge Base Loaded: {len(kb)} files")

    # Test search functionality
    print("\n🔍 Testing search functionality...")
    test_queries = [
        "coconut care tips",
        "paddy irrigation",
        "pest control",
        "fertilizer management"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = processor.search_knowledge(query, kb, top_k=3)
        print(f"Found {len(results)} results")
        
        for i, r in enumerate(results[:2], 1):
            print(f"  {i}. [{r['score']}] {r['filename']} - {r['tags']}")
            print(f"     Snippet: {r['snippet'][:100]}...")
    
    print("\n✅ Testing completed successfully!")
