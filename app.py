from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import sys

# This ensures Python can find your utils.py file in the same folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import extract_features

app = Flask(__name__)
CORS(app)  # This allows your frontend website to talk to this Python backend

# 1. Load the AI Model (the .pkl file)
model_path = os.path.join(os.path.dirname(__file__), 'phishing_model.pkl')

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("ERROR: phishing_model.pkl not found! Run train.py first.")

@app.route('/predict', methods=['POST'])
def predict():
    # Get the data sent from the frontend
    data = request.get_json()
    url = data.get('url', '').lower()
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # --- STEP A: MANUAL SECURITY CHECK (Heuristics) ---
    # These are immediate "Red Flags" that the AI might miss
    suspicious_triggers = ['free', 'iphone', 'win', 'prize', 'gift', 'login', 'verify', 'tk', 'ml', 'ga', 'update', 'billing']
    
    manual_flag = False
    for word in suspicious_triggers:
        if word in url:
            manual_flag = True
            break

    # --- STEP B: AI PREDICTION ---
    # We turn the URL into numbers (features) and ask the AI
    features = [extract_features(url)]
    prediction = model.predict(features)[0]
    
    # --- STEP C: FINAL DECISION ---
    # If the AI says it's bad (1) OR our manual check found a trigger word...
    if prediction == 1 or manual_flag == True:
        result = "PHISHING"
    else:
        result = "SAFE"
        
    print(f"URL Checked: {url} | Result: {result}") # This prints in your terminal
    return jsonify({'result': result, 'url': url})

if __name__ == '__main__':
    print("------------------------------------------")
    print("Phishing Detector Server is now STARTING!")
    print("Ready to receive URLs from your website.")
    print("------------------------------------------")
    app.run(debug=True, port=5000)