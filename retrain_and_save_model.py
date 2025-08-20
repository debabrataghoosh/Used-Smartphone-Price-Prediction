import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Load your training data
# Adjust the path and columns as needed
df = pd.read_csv('data/processed/resale.csv')

# Encode categorical features
brand_encoder = LabelEncoder()
df['brand_encoded'] = brand_encoder.fit_transform(df['brand_name'])

# Features and target - matching exactly what app.py expects
features = [
    'storage', 'RAM', 'age',
    'screen_condition_encoded', 'body_condition_encoded', 'water_damage', 
    'battery_health', 'core_feature_faulty', 'has_full_kit',
    'brand_encoded', 'warranty_status_extended', 'warranty_status_out_of_warranty'
]

# Convert boolean columns to int if needed
for col in ['water_damage', 'core_feature_faulty', 'has_full_kit']:
    if df[col].dtype == bool:
        df[col] = df[col].astype(int)

# Encode screen_condition and body_condition as app.py does
screen_mapping = {'Good': 3, 'Scratched': 2, 'Cracked': 1}
body_mapping = {'Good': 3, 'Scratched': 2, 'Damaged': 1}

df['screen_condition_encoded'] = df['screen_condition'].map(screen_mapping)
df['body_condition_encoded'] = df['body_condition'].map(body_mapping)

# Create warranty status one-hot encoding as app.py does
df['warranty_status_extended'] = (df['warranty_status'] == 'Extended Warranty').astype(int)
df['warranty_status_out_of_warranty'] = (df['warranty_status'] == 'Out of Warranty').astype(int)

# Prepare final features array
X = df[features].values
y = df['resale_price'].values

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model and encoders
with open('models/final_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('models/brand_encoder.pkl', 'wb') as f:
    pickle.dump(brand_encoder, f)

print('Model and encoders saved to models/.')
print(f'Model trained with {len(features)} features: {features}')
print(f'Training data shape: {X.shape}')
print(f'Model score: {model.score(X, y):.4f}')
