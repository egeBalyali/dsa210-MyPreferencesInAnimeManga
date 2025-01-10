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

def get_one_anime_info(anime_id):
    """Fetch anime info from MyAnimeList API for the given anime ID."""
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
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    url = f"{BASE_URL}{anime_id}?fields=mean,num_episodes,rating,genres"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch data for anime ID {anime_id}: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract URL from form data
    url = request.form['url']
    match = re.search(r'(\d+)', url)  # Extract anime_id (adjust regex for your URL structure)
    if not match:
        return jsonify({'error': 'Invalid URL'}), 400

    anime_id = match.group(1)
    try:
        # Fetch anime info from the API
        anime_info = get_one_anime_info(anime_id)

        # Prepare data for prediction
        mean = anime_info.get('mean', 0)
        num_episodes = anime_info.get('num_episodes', 0)
        rating = anime_info.get('rating', 'Unknown')
        genres = anime_info.get('genres', [])

        # Convert genres to one-hot encoded columns
        genre_columns = {f'genre_{genre["name"]}': 1 for genre in genres}
        all_features = {
            'mean': mean,
            'num_episodes': num_episodes,
            'rating': rating,
            **genre_columns
        }

        # Convert to DataFrame and align with model features
        feature_df = pd.DataFrame([all_features])
        feature_df = feature_df.reindex(columns=model.named_steps['preprocessor'].feature_names_in_, fill_value=0)

        # Predict the score
        predicted_score = model.predict(feature_df)[0]
        if (predicted_score > 10):
            predicted_score = 10
        return jsonify({'anime_id': anime_id, 'predicted_score': predicted_score})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
