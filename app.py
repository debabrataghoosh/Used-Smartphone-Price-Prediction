from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'smartphone_price_prediction_secret_key_2024'
CORS(app)

# Load the training data to get actual options
def load_training_data():
    """Load the training data to get actual available options"""
    try:
        data_path = os.path.join('data', 'processed', 'resale.csv')
        df = pd.read_csv(data_path)
        
        # Extract unique values for each feature
        data_info = {
            'brands': sorted(df['brand_name'].unique()),
            'storage_options': sorted(df['storage'].unique()),
            'ram_options': sorted(df['RAM'].unique()),
            'warranty_status': sorted(df['warranty_status'].unique()),
            'screen_conditions': sorted(df['screen_condition'].unique()),
            'body_conditions': sorted(df['body_condition'].unique()),
            'water_damage': [False, True],
            'battery_health_range': {'min': int(df['battery_health'].min()), 'max': int(df['battery_health'].max())},
            'core_feature_faulty': [False, True],
            'has_full_kit': [False, True],
            'age_range': {'min': int(df['age'].min()), 'max': int(df['age'].max())}
        }
        
        # Get brand-specific models
        brand_models = {}
        for brand in data_info['brands']:
            brand_models[brand] = sorted(df[df['brand_name'] == brand]['Name'].unique())
        
        data_info['brand_models'] = brand_models
        
        logger.info("Training data loaded successfully")
        return data_info
        
    except Exception as e:
        logger.error(f"Error loading training data: {e}")
        return None

# Load models and encoders
def load_models():
    """Load the trained ML models and encoders"""
    models = {}
    try:
        # Load the final model
        if os.path.exists('models/final_model.pkl'):
            with open('models/final_model.pkl', 'rb') as f:
                models['final_model'] = pickle.load(f)
            logger.info("Final model loaded successfully")
        
        # Load brand encoder
        if os.path.exists('models/brand_encoder.pkl'):
            with open('models/brand_encoder.pkl', 'rb') as f:
                models['brand_encoder'] = pickle.load(f)
            logger.info("Brand encoder loaded successfully")
            
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        models = {}
    
    return models

# Initialize data and models
training_data = load_training_data()
models = load_models()

@app.route('/api/brands')
def get_brands():
    """Get available brands"""
    if training_data:
        return jsonify({'brands': training_data['brands']})
    return jsonify({'error': 'Training data not available'}), 500

@app.route('/api/models/<brand>')
def get_models_for_brand(brand):
    """Get models for a specific brand"""
    if training_data and brand in training_data['brand_models']:
        return jsonify({'models': training_data['brand_models'][brand]})
    return jsonify({'error': 'Brand not found'}), 404

@app.route('/api/options')
def get_all_options():
    """Get all available options for the form"""
    if training_data:
        return jsonify({
            'storage_options': training_data['storage_options'],
            'ram_options': training_data['ram_options'],
            'warranty_status': training_data['warranty_status'],
            'screen_conditions': training_data['screen_conditions'],
            'body_conditions': training_data['body_conditions'],
            'water_damage': training_data['water_damage'],
            'battery_health_range': training_data['battery_health_range'],
            'core_feature_faulty': training_data['core_feature_faulty'],
            'has_full_kit': training_data['has_full_kit'],
            'age_range': training_data['age_range']
        })
    return jsonify({'error': 'Training data not available'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Handle price prediction requests"""
    try:
        # Get form data
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'brand', 'name', 'storage', 'ram', 'age',
            'warranty_status', 'screen_condition', 'body_condition',
            'water_damage', 'battery_health', 'core_feature_faulty', 'has_full_kit'
        ]
        
        for field in required_fields:
            if field not in data or data[field] in [None, '']:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Extract and validate features
        brand = str(data['brand']).strip()
        name = str(data['name']).strip()
        storage = float(data['storage'])
        ram = float(data['ram'])
        age = int(data['age'])
        warranty_status = str(data['warranty_status']).strip()
        screen_condition = str(data['screen_condition']).strip()
        body_condition = str(data['body_condition']).strip()
        water_damage = bool(data['water_damage'])
        battery_health = float(data['battery_health'])
        core_feature_faulty = bool(data['core_feature_faulty'])
        has_full_kit = bool(data['has_full_kit'])
        
        # Validate against actual training data
        if not training_data:
            return jsonify({'error': 'Training data not available'}), 500
        
        if brand not in training_data['brands']:
            return jsonify({'error': f'Invalid brand: {brand}'}), 400
        
        if name not in training_data['brand_models'].get(brand, []):
            return jsonify({'error': f'Invalid model for brand {brand}: {name}'}), 400
        
        if storage not in training_data['storage_options']:
            return jsonify({'error': f'Invalid storage: {storage}'}), 400
        
        if ram not in training_data['ram_options']:
            return jsonify({'error': f'Invalid RAM: {ram}'}), 400
        
        if age < training_data['age_range']['min'] or age > training_data['age_range']['max']:
            return jsonify({'error': f'Age must be between {training_data["age_range"]["min"]} and {training_data["age_range"]["max"]} months'}), 400
        
        if warranty_status not in training_data['warranty_status']:
            return jsonify({'error': f'Invalid warranty status: {warranty_status}'}), 400
        
        if screen_condition not in training_data['screen_conditions']:
            return jsonify({'error': f'Invalid screen condition: {screen_condition}'}), 400
        
        if body_condition not in training_data['body_conditions']:
            return jsonify({'error': f'Invalid body condition: {body_condition}'}), 400
        
        if battery_health < training_data['battery_health_range']['min'] or battery_health > training_data['battery_health_range']['max']:
            return jsonify({'error': f'Battery health must be between {training_data["battery_health_range"]["min"]} and {training_data["battery_health_range"]["max"]}'}), 400
        
        # Prepare features for prediction
        features = prepare_features(
            brand, name, storage, ram, age, warranty_status, 
            screen_condition, body_condition, water_damage, 
            battery_health, core_feature_faulty, has_full_kit
        )
        
        if features is None:
            return jsonify({'error': 'Error preparing features for prediction'}), 500
        
        # Make prediction
        if 'final_model' in models:
            prediction = models['final_model'].predict(features.reshape(1, -1))[0]
            confidence = calculate_confidence(features)
            
            # Format prediction
            predicted_price = max(0, round(prediction, 2))
            
            return jsonify({
                'success': True,
                'predicted_price': predicted_price,
                'confidence': confidence,
                'features_used': {
                    'brand': brand,
                    'name': name,
                    'storage': f"{storage} GB",
                    'ram': f"{ram} GB",
                    'age': f"{age} months",
                    'warranty_status': warranty_status,
                    'screen_condition': screen_condition,
                    'body_condition': body_condition,
                    'water_damage': water_damage,
                    'battery_health': f"{battery_health}%",
                    'core_feature_faulty': core_feature_faulty,
                    'has_full_kit': has_full_kit
                }
            })
        else:
            return jsonify({'error': 'Model not available'}), 500
            
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': 'Internal server error during prediction'}), 500

def prepare_features(brand, name, storage, ram, age, warranty_status, 
                    screen_condition, body_condition, water_damage, 
                    battery_health, core_feature_faulty, has_full_kit):
    """Prepare features for model prediction using actual training data structure"""
    try:
        # Initialize feature array
        features = []
        
        # 1. Storage (GB)
        features.append(storage)
        
        # 2. RAM (GB)
        features.append(ram)
        
        # 3. Age in months
        features.append(age)
        
        # 4. Screen condition (encoded)
        screen_mapping = {'Good': 3, 'Scratched': 2, 'Cracked': 1}
        features.append(screen_mapping.get(screen_condition, 2))
        
        # 5. Body condition (encoded)
        body_mapping = {'Good': 3, 'Scratched': 2, 'Damaged': 1}
        features.append(body_mapping.get(body_condition, 2))
        
        # 6. Water damage (boolean to int)
        features.append(1 if water_damage else 0)
        
        # 7. Battery health (percentage)
        features.append(battery_health)
        
        # 8. Core feature faulty (boolean to int)
        features.append(1 if core_feature_faulty else 0)
        
        # 9. Has full kit (boolean to int)
        features.append(1 if has_full_kit else 0)
        
        # 10. Brand name encoded
        if 'brand_encoder' in models:
            try:
                brand_encoded = models['brand_encoder'].transform([brand])[0]
                features.append(brand_encoded)
            except:
                features.append(0)
        else:
            features.append(0)
        
        # 11. Warranty status - Extended Warranty (one-hot encoded)
        features.append(1 if warranty_status == 'Extended Warranty' else 0)
        
        # 12. Warranty status - Out of Warranty (one-hot encoded)
        features.append(1 if warranty_status == 'Out of Warranty' else 0)
        
        # Ensure we have exactly 12 features
        if len(features) != 12:
            logger.error(f"Expected 12 features, got {len(features)}")
            return None
            
        return np.array(features)
        
    except Exception as e:
        logger.error(f"Feature preparation error: {e}")
        return None

def calculate_confidence(features):
    """Calculate prediction confidence based on feature values"""
    try:
        # Simple confidence calculation based on feature ranges
        confidence = 0.8  # Base confidence
        
        # Adjust based on age (newer phones = higher confidence)
        age = features[2]  # Age is at index 2
        if age <= 2:
            confidence += 0.1
        elif age >= 4:
            confidence -= 0.05
        
        # Adjust based on condition (screen/body condition)
        screen_condition = features[3]  # Screen condition is at index 3
        body_condition = features[4]    # Body condition is at index 4
        
        if screen_condition >= 3 and body_condition >= 3:
            confidence += 0.05
        elif screen_condition <= 1 or body_condition <= 1:
            confidence -= 0.1
        
        # Adjust based on battery health
        battery_health = features[6]  # Battery health is at index 6
        if battery_health >= 90:
            confidence += 0.05
        elif battery_health <= 80:
            confidence -= 0.05
        
        return min(0.95, max(0.6, confidence))
        
    except:
        return 0.8

@app.route('/health')
def health_check():
    """Health check endpoint"""
    model_status = 'final_model' in models
    data_status = training_data is not None
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_status,
        'training_data_loaded': data_status,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Check if models and training data are loaded
    if not models:
        logger.error("No models loaded. Please check model files.")
        exit(1)
    
    if not training_data:
        logger.error("Training data not loaded. Please check resale.csv file.")
        exit(1)
    
    port = 8501
    debug = False
    
    logger.info(f"Starting Smartphone Price Predictor on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
