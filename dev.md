# AgriAssist Development to Production Checklist

## 🚨 CRITICAL: Code/Configurations to Remove Before Production

This document outlines all development-specific code, configurations, and security vulnerabilities that MUST be addressed before deploying to production.

---

## 🔐 **SECURITY VULNERABILITIES (CRITICAL)**

### 1. **Hardcoded API Keys** ⚠️ **IMMEDIATE REMOVAL REQUIRED**
**Files to modify:**
- `backend/app.py` (Line 23)
- `js/config.js` (Line 26)
- `pages/homepage_ai_query_interface.html` (Line 969)

**Current vulnerable code:**
```python
# backend/app.py
os.environ["GOOGLE_API_KEY"] = "AIzaSyCWK3gI22NlZXOqNFSpj8ag3yR752uj6tU"
```

```javascript
// js/config.js
apiKey: 'AIzaSyCWK3gI22NlZXOqNFSpj8ag3yR752uj6tU', // Your Gemini API key
```

**Production fix:**
```python
# backend/app.py
import os
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is required")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
```

```javascript
// js/config.js - Remove hardcoded API key
apis: {
    gemini: {
        apiKey: process.env.GOOGLE_API_KEY || '', // Use environment variable
        model: 'gemini-1.5-flash',
        maxTokens: 2048
    }
}
```

---

## 🌐 **DEVELOPMENT-SPECIFIC CONFIGURATIONS**

### 2. **Hardcoded Local IP Addresses** ⚠️ **MUST CHANGE**
**Files to modify:**
- `js/config.js` (Lines 12, 17)
- `simple_agriassist.html` (Line 211)
- `test_network.html` (Lines 27, 28, 29, 42, 99, 115)

**Current development code:**
```javascript
// js/config.js
baseUrl: 'http://172.20.10.3:3000', // Local MacBook IP
```

**Production fix:**
```javascript
// js/config.js
baseUrl: process.env.REACT_APP_API_URL || 'https://your-production-domain.com/api',
```

### 3. **Debug Mode Enabled** ⚠️ **SECURITY RISK**
**File to modify:**
- `backend/app.py` (Line 285)

**Current development code:**
```python
app.run(debug=True, port=3000, host='0.0.0.0')
```

**Production fix:**
```python
app.run(debug=False, port=int(os.getenv('PORT', 5000)), host='0.0.0.0')
```

---

## 🧹 **DEVELOPMENT-ONLY FILES TO REMOVE**

### 4. **Test and Debug Files** (Already cleaned up ✅)
**Files that were removed:**
- `backend/test_cors.py`
- `backend/test_function.py`
- `backend/test_gemini.py`
- `backend/test_pdf_connection.py`
- `backend/example_usage.py`
- `backend/quick_setup.py`
- `backend/server.log`

### 5. **Development Documentation Files** (Keep for reference, remove from production)
**Files to exclude from production build:**
- `test_network.html` - Development testing file
- `debug_connection.html` - Debug file
- `force_refresh.html` - Cache testing file
- `COMPLETE_SETUP_GUIDE.md` - Development setup guide
- `setup-for-beginners.md` - Development guide
- `WEATHER_SETUP_GUIDE.md` - Development guide
- `backend/deploy_with_pdf.md` - Deployment documentation
- `backend/deploy-backend.md` - Deployment documentation
- `backend/README_PDF_SETUP.md` - Setup documentation

---

## 🔧 **CONFIGURATION CHANGES FOR PRODUCTION**

### 6. **CORS Configuration** ⚠️ **SECURITY CONCERN**
**Current development code:**
```python
CORS(app, 
     origins="*",  # ⚠️ Allows all origins - SECURITY RISK
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers", "Access-Control-Allow-Methods"],
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
     supports_credentials=False)
```

**Production fix:**
```python
CORS(app, 
     origins=["https://your-production-domain.com", "https://www.your-production-domain.com"],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"],
     supports_credentials=False)
```

### 7. **Logging Configuration** ⚠️ **INFORMATION LEAKAGE**
**Current development code:**
```python
logging.basicConfig(level=logging.INFO)  # ⚠️ Too verbose for production
```

**Production fix:**
```python
logging.basicConfig(level=logging.WARNING)  # Only log warnings and errors
```

---

## 📁 **ENVIRONMENT VARIABLES TO SET**

### 8. **Required Environment Variables for Production**
Create a `.env` file or set these in your production environment:

```bash
# Required
GOOGLE_API_KEY=your_actual_gemini_api_key_here
FLASK_ENV=production
FLASK_DEBUG=False

# Optional
PORT=5000
API_URL=https://your-production-domain.com/api
FRONTEND_URL=https://your-production-domain.com
```

---

## 🚀 **PRODUCTION DEPLOYMENT CHECKLIST**

### 9. **Pre-Deployment Steps**
- [ ] Remove all hardcoded API keys
- [ ] Replace local IP addresses with production domains
- [ ] Set `debug=False` in Flask app
- [ ] Configure proper CORS origins
- [ ] Set up environment variables
- [ ] Remove development-only files
- [ ] Update logging level to WARNING
- [ ] Test with production-like environment

### 10. **Post-Deployment Verification**
- [ ] Verify API keys are not exposed in source code
- [ ] Test CORS with production domains only
- [ ] Confirm debug mode is disabled
- [ ] Check that no development URLs are accessible
- [ ] Verify logging is appropriate for production
- [ ] Test all API endpoints work correctly

---

## ⚠️ **CRITICAL SECURITY NOTES**

1. **API Key Exposure**: The current hardcoded API key is visible in the repository and should be considered compromised. Generate a new API key for production.

2. **CORS Misconfiguration**: Allowing all origins (`*`) is a security risk. Always specify exact production domains.

3. **Debug Mode**: Never run Flask in debug mode in production as it exposes sensitive information.

4. **Local IP Exposure**: Hardcoded local IPs will not work in production and expose internal network information.

---

## 📝 **FILES MODIFIED DURING CLEANUP**

The following duplicate files were removed to prevent conflicts:
- `backend/alternative_backend.py`
- `backend/app_simple_backup.py`
- `backend/app_simple.py`
- `backend/app_with_pdf.py`
- `backend/fast_backend.py`
- `backend/instant_backend.py`
- `backend/simple_backend.py`
- `backend/testsprite_backend.py`
- `backend/working_backend.py`

**Status**: ✅ Cleanup completed successfully - no more overlapping functions or duplicate code.

---

**Last Updated**: 2025-09-11
**Status**: Ready for production deployment after addressing security issues
