#!/bin/bash

# AgriAssist Deployment Script
echo "🚀 Starting AgriAssist Deployment..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: AgriAssist with advanced features"
fi

# Build CSS if needed
echo "🎨 Building CSS..."
if command -v npm &> /dev/null; then
    npm run build:css 2>/dev/null || echo "⚠️  CSS build skipped (npm not available)"
else
    echo "⚠️  npm not found, skipping CSS build"
fi

# Create production config
echo "⚙️  Creating production configuration..."
cp js/config.js js/config.prod.js

# Update production config
sed -i.bak 's/environment: '\''development'\''/environment: '\''production'\''/g' js/config.prod.js
sed -i.bak 's/baseUrl: '\''http:\/\/127.0.0.1:5000'\''/baseUrl: '\''https:\/\/your-backend-domain.com'\''/g' js/config.prod.js

echo "✅ Production configuration created!"

# Show deployment options
echo ""
echo "🌐 Choose your deployment method:"
echo "1. GitHub Pages (Free)"
echo "2. Netlify (Easy drag & drop)"
echo "3. Vercel (Fast & modern)"
echo "4. Your own server"
echo ""

# GitHub Pages setup
echo "📋 For GitHub Pages:"
echo "1. Create a new repository on GitHub"
echo "2. Run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/agriassist.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo "3. Go to Settings > Pages > Deploy from branch > main"
echo "4. Your site will be live at: https://YOUR_USERNAME.github.io/agriassist"
echo ""

# Netlify setup
echo "📋 For Netlify:"
echo "1. Go to https://netlify.com"
echo "2. Drag this folder to the deploy area"
echo "3. Your site will be live instantly!"
echo ""

# Vercel setup
echo "📋 For Vercel:"
echo "1. Install Vercel CLI: npm i -g vercel"
echo "2. Run: vercel"
echo "3. Follow the prompts"
echo ""

echo "🔧 Don't forget to:"
echo "1. Update your backend URL in js/config.js"
echo "2. Add your Gemini API key"
echo "3. Configure CORS on your backend server"
echo "4. Test all features after deployment"
echo ""

echo "✅ Deployment preparation complete!"
