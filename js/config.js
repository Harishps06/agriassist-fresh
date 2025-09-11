// AgriAssist Configuration
// Update these settings for different environments
// Version: 2025-09-11-v5 - Fixed backend connection to port 8888

const CONFIG = {
    // Environment: 'development' or 'production'
    environment: 'development',
    
    // API Configuration
    api: {
        development: {
            baseUrl: 'http://localhost:8888',
            timeout: 30000,
            retryAttempts: 3
        },
        production: {
            baseUrl: 'https://agriassist-fresh.onrender.com', // Your actual Render backend URL
            timeout: 30000,
            retryAttempts: 3
        }
    },
    
    // External API Keys
    apis: {
        gemini: {
            apiKey: 'AIzaSyCWK3gI22NlZXOqNFSpj8ag3yR752uj6tU', // Your Gemini API key
            model: 'gemini-1.5-flash',
            maxTokens: 2048
        },
        weather: {
            apiKey: 'YOUR_WEATHER_API_KEY', // Get from OpenWeatherMap
            baseUrl: 'https://api.openweathermap.org/data/2.5'
        }
    },
    
    // App Settings
    app: {
        name: 'AgriAssist',
        version: '2.0.0',
        defaultLanguage: 'en-US',
        supportedLanguages: ['en-US', 'ml-IN'],
        maxFileSize: 10 * 1024 * 1024, // 10MB
        supportedImageFormats: ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
    },
    
    // Feature Flags
    features: {
        voiceRecognition: true,
        imageAnalysis: true,
        offlineMode: true,
        pushNotifications: true,
        weatherWidget: true,
        cropCalculator: true
    },
    
    // PWA Settings
    pwa: {
        name: 'AgriAssist - AI Farming Assistant',
        shortName: 'AgriAssist',
        description: 'AI-powered agricultural assistance for Kerala farmers',
        themeColor: '#2D5016',
        backgroundColor: '#F7F9F4',
        startUrl: '/',
        scope: '/',
        display: 'standalone',
        orientation: 'portrait'
    }
};

// Get current configuration based on environment
function getConfig() {
    const env = CONFIG.environment;
    return {
        ...CONFIG,
        api: CONFIG.api[env],
        isDevelopment: env === 'development',
        isProduction: env === 'production'
    };
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CONFIG, getConfig };
} else {
    window.AgriAssistConfig = { CONFIG, getConfig };
}
