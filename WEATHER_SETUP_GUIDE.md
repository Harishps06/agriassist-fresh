# 🌤️ Weather & Calendar Setup Guide

## **Weather API Setup**

### **Step 1: Get OpenWeatherMap API Key**

1. **Visit OpenWeatherMap**: Go to [https://openweathermap.org/api](https://openweathermap.org/api)
2. **Sign Up**: Create a free account
3. **Get API Key**: 
   - Go to "My API Keys" section
   - Copy your API key
   - Free tier allows 1,000 calls/day

### **Step 2: Update Configuration**

1. **Open `js/config.js`**
2. **Replace the API key**:
   ```javascript
   weather: {
       apiKey: '91fb443053c8a172e55c1b1b4bf63fe6', // Replace this
       baseUrl: 'https://api.openweathermap.org/data/2.5'
   }
   ```

### **Step 3: Test the Weather Widget**

1. **Open your website**: `http://localhost:8000/pages/homepage_ai_query_interface.html`
2. **Check the weather widget** at the top of the page
3. **Verify it shows real weather data** for Kerala

## **Features Included**

### **🌤️ Weather Widget**
- **Real-time weather** for Kerala, India
- **Temperature, humidity, wind speed**
- **Weather icons** (sunny, cloudy, rainy, etc.)
- **Auto-updates every 30 minutes**
- **Fallback data** if API fails

### **📅 Agricultural Calendar**
- **Kerala-specific seasons**:
  - **Kharif** (June-October): Monsoon, rice planting
  - **Rabi** (November-February): Winter, wheat & pulses
  - **Summer** (March-May): Hot season, mango & cashew
- **Current date display**
- **Season-appropriate activities**
- **Next activity suggestions**

### **💡 Daily Agricultural Tips**
- **Randomized tips** based on current season
- **Weather-based advice**
- **Updates every hour**
- **Kerala farming practices**

## **Customization Options**

### **Change Location**
```javascript
// In WeatherService constructor
this.location = { lat: YOUR_LAT, lon: YOUR_LON };
```

### **Update Seasons**
```javascript
// In AgriculturalCalendarService.getKeralaSeasons()
// Modify month ranges and activities
```

### **Add More Tips**
```javascript
// In AgriculturalCalendarService.getAgriculturalTips()
// Add more tips to the array
```

## **Troubleshooting**

### **Weather Not Loading**
1. **Check API key** is correct
2. **Verify internet connection**
3. **Check browser console** for errors
4. **Ensure API key has permissions**

### **Calendar Not Updating**
1. **Check system date/time**
2. **Verify JavaScript is enabled**
3. **Clear browser cache**

### **Mobile Issues**
1. **Test on different devices**
2. **Check responsive design**
3. **Verify touch interactions**

## **API Limits & Costs**

### **OpenWeatherMap Free Tier**
- **1,000 calls/day**
- **Current weather only**
- **5-day forecast**
- **No credit card required**

### **Upgrade Options**
- **Pro**: $40/month for 100,000 calls/day
- **Business**: $160/month for 1M calls/day
- **Enterprise**: Custom pricing

## **Alternative Weather APIs**

If OpenWeatherMap doesn't work:

1. **AccuWeather**: [https://developer.accuweather.com/](https://developer.accuweather.com/)
2. **WeatherAPI**: [https://www.weatherapi.com/](https://www.weatherapi.com/)
3. **Weatherbit**: [https://www.weatherbit.io/](https://www.weatherbit.io/)

## **Next Steps**

1. **Get your API key** from OpenWeatherMap
2. **Update the config file**
3. **Test the weather widget**
4. **Customize for your needs**
5. **Deploy to production**

Your weather and calendar system is now ready! 🌱📅
