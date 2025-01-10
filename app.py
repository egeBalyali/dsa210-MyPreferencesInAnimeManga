import pickle
import json
import re
from flask import Flask, request, render_template, jsonify
import joblib
import requests
import pandas as pd

# Flask app setup
app = Flask(__name__)

# Load the pre-trained regression model
model = joblib.load('anime_score_predictor.pkl')

# Token file and API base URL
TOKEN_FILE_PATH = './token.json'
BASE_URL = 'https://api.myanimelist.net/v2/anime/'


def get_anime_info(anime_id):
    try:
        with open(TOKEN_FILE_PATH, 'r', encoding='utf-8') as token_file:
            token_data = json.load(token_file)
            access_token = token_data.get('access_token')
            if not access_token:
                raise ValueError("No 'access_token' found in token.json")
    except FileNotFoundError:
        raise FileNotFoundError(f"Token file not found: {TOKEN_FILE_PATH}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in token file: {TOKEN_FILE_PATH}")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f"{BASE_URL}{anime_id}?fields=mean,num_episodes,rating,genres,main_picture"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form.get('url')
    anime_id = url.split('/')[-2]  # Extract the ID from the URL

    # Fetch anime info
    try:
        anime_info = get_anime_info(anime_id)
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch anime info: {str(e)}"}), 400

    # Extract required fields
    mean = anime_info.get('mean', 0)
    num_episodes = anime_info.get('num_episodes', 0)
    rating = anime_info.get('rating', 'None')
    genres = [genre['name'] for genre in anime_info.get('genres', [])]
    main_picture = anime_info.get('main_picture', {}).get('large', '')

    # Generate prediction (dummy logic here; replace with model prediction)
    # Load your saved model if needed
    predicted_score = mean + 0.1  # Placeholder logic

    return jsonify({
        "anime_id": anime_id,
        "predicted_score": predicted_score,
        "main_picture": main_picture,
        "mean": mean,
        "num_episodes": num_episodes,
        "rating": rating,
        "genres": genres
    })

if __name__ == '__main__':
    app.run(debug=True)
