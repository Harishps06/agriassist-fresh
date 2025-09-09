# AgriAssist Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: GitHub Pages (Recommended - Free)
1. Create a new repository on GitHub
2. Push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/agriassist.git
   git branch -M main
   git push -u origin main
   ```
3. Go to repository Settings > Pages
4. Select "Deploy from a branch" > main > / (root)
5. Your site will be live at: `https://YOUR_USERNAME.github.io/agriassist`

### Option 2: Netlify (Easy Drag & Drop)
1. Go to https://netlify.com
2. Drag your project folder to the deploy area
3. Your site will be live instantly with a custom URL

### Option 3: Vercel (Fast & Modern)
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel` in your project directory
3. Follow the prompts

### Option 4: Your Own Server
1. Upload files to your web server
2. Configure web server to serve static files
3. Set up HTTPS for PWA features

## 🔧 Backend Configuration

### Update API Endpoints
Replace `http://127.0.0.1:5000` with your production backend URL in:
- `pages/homepage_ai_query_interface.html` (line ~1147)
- Any other files that make API calls

### Environment Variables
Create a config file for different environments:
```javascript
const config = {
  development: {
    apiUrl: 'http://127.0.0.1:5000',
    geminiApiKey: 'dev-key'
  },
  production: {
    apiUrl: 'https://your-backend-domain.com',
    geminiApiKey: 'prod-key'
  }
};
```

## 🔑 API Keys Setup

### Gemini Vision API
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Replace `YOUR_GEMINI_API_KEY` in the code

### Backend Server
Ensure your backend server:
1. Has CORS enabled for your domain
2. Handles the enhanced request format
3. Is accessible via HTTPS in production

## 📱 PWA Features
Your site includes PWA features that require HTTPS in production:
- Service Worker
- Push Notifications
- Offline functionality
- Install prompts

## 🌐 Custom Domain (Optional)
1. Buy a domain name
2. Configure DNS to point to your hosting provider
3. Update manifest.json with your domain
4. Set up SSL certificate

## 🔍 Testing Checklist
- [ ] Voice recognition works
- [ ] Image analysis works
- [ ] Backend API calls succeed
- [ ] PWA installs on mobile
- [ ] Offline mode works
- [ ] All pages load correctly
- [ ] Mobile responsiveness
- [ ] Malayalam text displays properly
