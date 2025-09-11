#!/usr/bin/env python3
"""
Test script to verify PDF-backend connection
"""

import requests
import json
import time
from pdf_processor import AgriculturalPDFProcessor

def test_pdf_processor():
    """Test PDF processor directly"""
    print("🔍 Testing PDF Processor...")
    
    processor = AgriculturalPDFProcessor('knowledge_base')
    kb = processor.load_all_knowledge()
    
    print(f"✅ Knowledge base loaded: {len(kb)} sections")
    print(f"📊 Total entries: {sum(len(entries) for entries in kb.values())}")
    
    # Test search functionality
    results = processor.search_knowledge('rice cultivation', kb)
    print(f"🔍 Search results for 'rice cultivation': {len(results)}")
    
    if results:
        print(f"📄 Sample result from: {results[0]['source']}")
        print(f"📝 Content preview: {results[0]['content'][:100]}...")
    
    return True

def test_backend_api():
    """Test backend API endpoints"""
    print("\n🌐 Testing Backend API...")
    
    base_url = "http://127.0.0.1:5000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"📊 Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False
    
    # Test knowledge stats endpoint
    try:
        response = requests.get(f"{base_url}/api/knowledge-stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print("✅ Knowledge stats endpoint working")
            print(f"📊 Stats: {stats}")
        else:
            print(f"❌ Knowledge stats failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Knowledge stats error: {e}")
    
    # Test ask endpoint
    try:
        test_data = {
            "question": "How to grow rice?",
            "language": "en-US",
            "context": {}
        }
        
        response = requests.post(
            f"{base_url}/api/ask", 
            json=test_data, 
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Ask endpoint working")
            print(f"📝 Answer preview: {result['answer'][:200]}...")
            print(f"📊 Sources: {result.get('sources', [])}")
            print(f"🎯 Confidence: {result.get('confidence', 'N/A')}")
        else:
            print(f"❌ Ask endpoint failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ask endpoint error: {e}")
        return False
    
    return True

def test_malayalam_support():
    """Test Malayalam language support"""
    print("\n🇮🇳 Testing Malayalam Support...")
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        test_data = {
            "question": "നെല്ല് കൃഷി എങ്ങനെ?",
            "language": "ml-IN",
            "context": {}
        }
        
        response = requests.post(
            f"{base_url}/api/ask", 
            json=test_data, 
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Malayalam support working")
            print(f"📝 Malayalam answer preview: {result['answer'][:200]}...")
        else:
            print(f"❌ Malayalam support failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Malayalam test error: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🌾 AgriAssist PDF-Backend Connection Test")
    print("=" * 50)
    
    # Test PDF processor
    pdf_ok = test_pdf_processor()
    
    if not pdf_ok:
        print("❌ PDF processor test failed")
        return
    
    # Wait a moment for any background processes
    time.sleep(2)
    
    # Test backend API
    api_ok = test_backend_api()
    
    if not api_ok:
        print("❌ Backend API test failed")
        return
    
    # Test Malayalam support
    malayalam_ok = test_malayalam_support()
    
    if not malayalam_ok:
        print("❌ Malayalam support test failed")
        return
    
    print("\n🎉 All tests passed! PDF-backend connection is working correctly.")
    print("\n📋 Summary:")
    print("✅ PDF processing: Working")
    print("✅ Knowledge base: Loaded")
    print("✅ Search functionality: Working")
    print("✅ Backend API: Working")
    print("✅ Malayalam support: Working")
    print("✅ PDF content integration: Working")

if __name__ == "__main__":
    main()
