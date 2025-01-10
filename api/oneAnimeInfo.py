import json
import os
import requests

# File paths
token_file_path = '../token.json'
base_url = 'https://api.myanimelist.net/v2/anime/'
def getOneAnimeInfo(anime_id):
    try:
        with open(token_file_path, 'r', encoding='utf-8') as token_file:
            token_data = json.load(token_file)
            access_token = token_data.get('access_token')
            if not access_token:
                raise ValueError("No 'access_token' found in token.json")
    except FileNotFoundError:
        raise FileNotFoundError(f"Token file not found: {token_file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in token file: {token_file_path}")
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    all_info = []
    url = f"{base_url}{anime_id}?fields=mean, num_episodes, rating, genres"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        anime_info = response.json()
        all_info.append(anime_info)
    except requests.RequestException as e:
        print(f"Failed to fetch data for anime ID {anime_id}: {e}")