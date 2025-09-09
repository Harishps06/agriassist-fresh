# 🌱 AgriAssist Setup Guide for Beginners

## 📋 What You Need
1. **GitHub Account** (free) - [github.com](https://github.com)
2. **VS Code** (you already have this)
3. **Your Backend Code** (from VS Code)
4. **API Keys** (I'll help you get these)

## 🚀 Step-by-Step Instructions

### Step 1: Create GitHub Account & Repository
1. Go to [github.com](https://github.com)
2. Click "Sign up" and create a free account
3. Click the "+" icon in top right → "New repository"
4. Name it: `agriassist`
5. Make it **Public** (for free GitHub Pages)
6. Click "Create repository"

### Step 2: Upload Your Code to GitHub
1. Open Terminal in VS Code (Terminal → New Terminal)
2. Copy and paste these commands one by one:

```bash
# Navigate to your project folder
cd /Users/harishps/Downloads/agriassist

# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/agriassist.git

# Push your code
git add .
git commit -m "Initial commit with all features"
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username**

### Step 3: Enable GitHub Pages
1. Go to your GitHub repository
2. Click "Settings" tab
3. Scroll down to "Pages" section
4. Under "Source", select "Deploy from a branch"
5. Select "main" branch and "/ (root)" folder
6. Click "Save"
7. Wait 2-3 minutes, then visit: `https://YOUR_USERNAME.github.io/agriassist`

### Step 4: Get API Keys

#### Gemini API Key (for image analysis):
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

#### Weather API Key (optional):
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for free account
3. Go to "API Keys" section
4. Copy your API key

### Step 5: Update Configuration
1. In VS Code, open `js/config.js`
2. Replace these lines:

```javascript
// Change this:
baseUrl: 'http://127.0.0.1:5000'

// To your backend URL (we'll set this up):
baseUrl: 'https://your-backend-domain.com'

// Add your API keys:
gemini: {
    apiKey: 'YOUR_ACTUAL_GEMINI_API_KEY_HERE'
},
weather: {
    apiKey: 'YOUR_ACTUAL_WEATHER_API_KEY_HERE'
}
```

### Step 6: Backend Integration
**This is where I need your backend code!**

Please share your backend code from VS Code, and I'll help you:
1. Update it to work with the frontend
2. Add CORS support
3. Handle the new request format
4. Deploy it online

## 🔍 Testing Your Website

### Test Voice Recognition:
1. Open your website
2. Click the microphone button (🎤)
3. Say "What is the best time to plant rice?"
4. Check if it transcribes correctly

### Test Image Analysis:
1. Click the camera button (📷)
2. Upload a plant photo
3. Wait for AI analysis
4. Check if you get agricultural insights

### Test Backend Connection:
1. Type a question in the text box
2. Press Enter
3. Check if you get a response from your backend

## 🆘 Common Issues & Solutions

### Issue: "Microphone access denied"
**Solution:** Click the microphone icon in your browser address bar and allow access

### Issue: "API request failed"
**Solution:** Check your backend URL in `js/config.js`

### Issue: "Image analysis not working"
**Solution:** Add your Gemini API key in `js/config.js`

### Issue: "Website not loading"
**Solution:** Check GitHub Pages deployment status in repository Settings

## 📞 Need Help?
1. Share your backend code with me
2. Tell me which step you're stuck on
3. I'll provide specific instructions for your situation

## 🎯 Next Steps After Setup
1. Test all features
2. Customize the design
3. Add more farming knowledge
4. Share with farmers
5. Get feedback and improve

---
**Remember:** Take it one step at a time. Don't rush! 🚀
