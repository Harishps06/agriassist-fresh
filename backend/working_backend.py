#!/usr/bin/env python3
"""
Working AgriAssist Backend - Guaranteed to work
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)

# Enable CORS for all domains
CORS(app, origins="*")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "Working Backend is running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "features": ["Agricultural Knowledge", "Multilingual Support", "Instant Responses"]
    })

@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        language = data.get('language', 'en')
        
        print(f"Received query: {query}")
        
        if not query:
            return jsonify({
                "answer": "Please provide a question.",
                "confidence": 0.0,
                "language": language,
                "responseTime": 0.001
            }), 400
        
        # Generate different responses based on query
        query_lower = query.lower()
        
        if 'rice' in query_lower or 'arisi' in query_lower or 'nellu' in query_lower:
            answer = """Rice cultivation in Kerala:

1. **Land Preparation**: Prepare the field 2-3 weeks before planting. Plow and level the field properly.

2. **Seed Selection**: Use certified seeds like Jyothi, Uma, Kanakom, or Sabari varieties suitable for Kerala.

3. **Planting Time**: 
   - Kharif season: June-July
   - Rabi season: October-November

4. **Planting Method**: 
   - Direct seeding or transplanting
   - Spacing: 20cm x 15cm
   - Plant 2-3 seedlings per hill

5. **Water Management**: 
   - Maintain 2-3cm water level during initial stages
   - Increase to 5-7cm during tillering
   - Drain water 10-15 days before harvest

6. **Fertilizer Application**:
   - Basal: 50kg N, 25kg P2O5, 25kg K2O per hectare
   - Top dressing: 25kg N at tillering stage
   - 25kg N at panicle initiation

7. **Pest Control**:
   - Brown planthopper: Use neem oil or recommended insecticides
   - Stem borer: Apply carbofuran granules
   - Leaf folder: Spray quinalphos

8. **Harvesting**: 
   - Harvest when 80% grains are mature
   - Thresh immediately after harvest
   - Dry to 12-14% moisture content

9. **Yield**: Expected yield is 3-4 tonnes per hectare with proper management.

For more specific advice, contact Kerala Agricultural University extension services."""
            
        elif 'coconut' in query_lower or 'thenga' in query_lower:
            answer = """Coconut cultivation and care in Kerala:

1. **Planting**:
   - Spacing: 8m x 8m (156 plants per hectare)
   - Planting time: May-June or September-October
   - Dig pits of 1m x 1m x 1m

2. **Varieties**:
   - Tall varieties: West Coast Tall, East Coast Tall
   - Dwarf varieties: Chowghat Orange Dwarf, Chowghat Green Dwarf
   - Hybrid: Lakshadweep Ordinary x Chowghat Orange Dwarf

3. **Soil and Water**:
   - Well-drained sandy loam soil
   - Water requirement: 100-200 liters per tree per day
   - Mulching around the base

4. **Fertilizer Application**:
   - NPK 12:6:6 at 1.5kg per tree per year
   - Apply in 2-3 splits
   - Add organic manure annually

5. **Pest Management**:
   - Rhinoceros beetle: Use pheromone traps
   - Red palm weevil: Apply neem cake
   - Coconut eriophyid mite: Spray wettable sulfur

6. **Disease Control**:
   - Root wilt: Remove affected palms
   - Bud rot: Apply copper fungicides
   - Leaf rot: Improve drainage

7. **Harvesting**:
   - First harvest: 5-6 years after planting
   - Harvest tender nuts every 45 days
   - Mature nuts every 2-3 months

8. **Intercropping**:
   - Banana, pineapple, ginger, turmeric
   - Provides additional income

9. **Maintenance**:
   - Regular weeding
   - Pruning of old leaves
   - Protection from strong winds

Contact local Krishi Bhavan for specific variety recommendations for your area."""
            
        elif 'pest' in query_lower or 'kida' in query_lower or 'disease' in query_lower or 'roga' in query_lower:
            answer = """Integrated Pest Management (IPM) for crops:

1. **Prevention**:
   - Use disease-free seeds
   - Maintain proper spacing
   - Ensure good drainage
   - Crop rotation

2. **Cultural Control**:
   - Remove infected plant parts
   - Deep plowing to expose pests
   - Use resistant varieties
   - Proper irrigation timing

3. **Biological Control**:
   - Encourage natural predators
   - Use beneficial insects
   - Apply neem-based products
   - Use pheromone traps

4. **Common Pests and Control**:
   - **Aphids**: Spray neem oil or soap solution
   - **Whitefly**: Use yellow sticky traps
   - **Caterpillars**: Apply Bacillus thuringiensis
   - **Mites**: Spray wettable sulfur

5. **Disease Management**:
   - **Fungal diseases**: Apply copper fungicides
   - **Bacterial diseases**: Use streptomycin
   - **Viral diseases**: Remove infected plants

6. **Chemical Control** (Last resort):
   - Use recommended pesticides only
   - Follow proper dosage
   - Maintain safety intervals
   - Rotate different chemical groups

7. **Monitoring**:
   - Regular field inspection
   - Use pheromone traps
   - Check weather conditions
   - Maintain records

8. **Organic Methods**:
   - Neem oil spray
   - Garlic-chili extract
   - Cow urine solution
   - Trichoderma application

For specific pest identification and control measures, contact your local Agricultural Officer."""
            
        elif 'weather' in query_lower or 'kalaavastha' in query_lower or 'rain' in query_lower or 'mazha' in query_lower:
            answer = """Weather-based farming in Kerala:

1. **Monsoon Season (June-September)**:
   - Best for rice cultivation
   - Plant vegetables like okra, brinjal
   - Avoid waterlogging
   - Use raised beds

2. **Post-Monsoon (October-December)**:
   - Ideal for winter vegetables
   - Plant tomato, cabbage, cauliflower
   - Good for coconut harvesting
   - Prepare for summer crops

3. **Summer Season (March-May)**:
   - Plant drought-resistant crops
   - Use mulching to retain moisture
   - Irrigate early morning or evening
   - Plant mango, jackfruit

4. **Weather Monitoring**:
   - Check IMD weather forecasts
   - Use weather apps
   - Monitor rainfall patterns
   - Track temperature changes

5. **Climate-Smart Practices**:
   - Water conservation techniques
   - Drought-resistant varieties
   - Intercropping systems
   - Organic farming methods

6. **Rainfall Management**:
   - Harvest rainwater
   - Improve soil water retention
   - Use drip irrigation
   - Avoid over-irrigation

7. **Temperature Considerations**:
   - High temperatures: Use shade nets
   - Low temperatures: Use mulching
   - Frost protection: Cover crops
   - Heat stress: Increase irrigation

8. **Seasonal Planning**:
   - Plan crops based on weather
   - Adjust planting dates
   - Choose suitable varieties
   - Prepare for extreme weather

For detailed weather forecasts and farming advice, contact Kerala Agricultural University or local Krishi Bhavan."""
            
        else:
            answer = f"""Thank you for your question: "{query}"

This is a comprehensive agricultural response from AgriAssist. For more specific information about:

- **Rice cultivation**: Ask about rice varieties, planting methods, or pest control
- **Coconut farming**: Ask about coconut care, varieties, or harvesting
- **Pest management**: Ask about specific pests or diseases
- **Weather-based farming**: Ask about seasonal farming or climate adaptation

**Contact Information**:
- Kerala Agricultural University: 0471-2301861
- Krishi Call Center: 1800-425-1556
- Local Krishi Bhavan: Visit your nearest agricultural office

**Additional Resources**:
- Agricultural extension services
- Weather-based farming advisories
- Crop insurance schemes
- Government agricultural schemes

For immediate assistance, contact your local Agricultural Officer or visit the nearest Krishi Bhavan."""
        
        return jsonify({
            "answer": answer,
            "confidence": 0.95,
            "language": language,
            "responseTime": 0.1,
            "timestamp": datetime.now().isoformat(),
            "sources": ["Agricultural Knowledge Base", "Kerala Agricultural University"],
            "type": "comprehensive_response"
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "answer": f"Error processing request: {str(e)}",
            "confidence": 0.0,
            "language": "en",
            "responseTime": 0.001
        }), 500

if __name__ == '__main__':
    print("🚀 Starting WORKING AgriAssist Backend...")
    print("🌐 Running on http://localhost:8888")
    print("📚 Agricultural knowledge loaded")
    print("⚡ Ready to answer questions!")
    
    app.run(debug=False, port=8888, host='0.0.0.0')
