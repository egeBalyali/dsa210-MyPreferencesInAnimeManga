import json
import os
import requests

# File paths
token_file_path = '../token.json'
input_json_path = '../data/EgeAnimeJSON.json'
output_json_path = '../anime/allInfo.json'

# API base URL
base_url = 'https://api.myanimelist.net/v2/anime/'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

# Step 1: Read the token
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

# Step 2: Read IDs from the input JSON file
try:
    with open(input_json_path, 'r', encoding='utf-8') as input_file:
        anime_data = json.load(input_file)
        anime_ids = [item['id'] for item in anime_data if item.get('id')]
        if not anime_ids:
            raise ValueError("No IDs found in the input JSON file")
except FileNotFoundError:
    raise FileNotFoundError(f"Input JSON file not found: {input_json_path}")
except json.JSONDecodeError:
    raise ValueError(f"Invalid JSON in input file: {input_json_path}")

# Step 3: Make API calls and collect data
headers = {
    'Authorization': f'Bearer {access_token}'
}
all_info = []

for anime_id in anime_ids:
    url = f"{base_url}{anime_id}?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        anime_info = response.json()
        all_info.append(anime_info)
    except requests.RequestException as e:
        print(f"Failed to fetch data for anime ID {anime_id}: {e}")

# Step 4: Save all data to the output JSON file
try:
    with open(output_json_path, 'w', encoding='utf-8') as output_file:
        json.dump(all_info, output_file, indent=4, ensure_ascii=False)
except Exception as e:
    raise RuntimeError(f"Failed to save output JSON file: {e}")

print(f"Anime information successfully saved to {output_json_path}")
