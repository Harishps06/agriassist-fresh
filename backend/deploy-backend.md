# Backend Deployment Guide

## 🚀 Deploy Your Backend to the Cloud

### Option 1: Railway (Recommended - Easy & Free)
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your agriassist repository
5. Railway will automatically detect it's a Python app
6. Add environment variable: `GOOGLE_API_KEY=your_api_key_here`
7. Deploy! Your backend will be live at: `https://your-app-name.railway.app`

### Option 2: Render (Free Tier Available)
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your repository
5. Set build command: `pip install -r backend/requirements.txt`
6. Set start command: `cd backend && python app.py`
7. Add environment variable: `GOOGLE_API_KEY=your_api_key_here`
8. Deploy!

### Option 3: Heroku (Paid but Reliable)
1. Install Heroku CLI
2. Run these commands:
```bash
cd backend
heroku create your-app-name
heroku config:set GOOGLE_API_KEY=your_api_key_here
git add .
git commit -m "Deploy backend"
git push heroku main
```

## 🔧 Local Testing

### Test your backend locally:
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Test the API:
```bash
curl -X POST http://127.0.0.1:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the best time to plant rice?"}'
```

## 📁 File Structure
```
backend/
├── app.py              # Your main Flask app
├── requirements.txt    # Python dependencies
├── knowledge_base/     # Your PDF and TXT files
└── db/                # Vector database (created automatically)
```

## 🔑 Environment Variables
- `GOOGLE_API_KEY`: Your Google API key for Gemini
- `PORT`: Port number (usually set automatically by hosting service)

## 🚨 Important Notes
1. **Never commit your API key** to GitHub
2. **Use environment variables** for sensitive data
3. **Test locally first** before deploying
4. **Check logs** if something goes wrong

## 🆘 Troubleshooting
- **Import errors**: Make sure all packages are in requirements.txt
- **API key errors**: Check your Google API key is correct
- **CORS errors**: Make sure Flask-CORS is installed and configured
- **Memory errors**: Your hosting service might have memory limits
