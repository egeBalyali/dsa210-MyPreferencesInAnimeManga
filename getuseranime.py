import json
import requests

# Load API token from output.json
def load_api_token(file_path):
    """
    Reads the API token from the specified JSON file.
    
    :param file_path: Path to the JSON file containing the API token.
    :return: The API token as a string.
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return data.get("access_token")
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")
    except json.JSONDecodeError:
        raise ValueError(f"File {file_path} is not a valid JSON file.")

# API endpoint
BASE_URL = "https://api.myanimelist.net/v2/users/@me/animelist"

def get_anime_list(api_token, status=None, sort=None, limit=100, offset=0):
    """
    Fetches the anime list of the user from MyAnimeList API.
    
    :param api_token: The API token for authorization.
    :param status: Filter anime list by status (e.g., "watching", "completed").
    :param sort: Sort the list by a specific field (e.g., "list_score", "anime_title").
    :param limit: The number of entries to retrieve (max 1000).
    :param offset: The offset for pagination.
    :return: The user's anime list as a JSON object.
    """
    
    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    params = {
        "fields": "list_status",  # Include list status in the results
        "limit": limit,
        "offset": offset
    }

    if status:
        params["status"] = status
    if sort:
        params["sort"] = sort

    response = requests.get(BASE_URL, headers = headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to fetch anime list. HTTP Status Code: {response.status_code}, Message: {response.text}"
        )

# Example usage
if __name__ == "__main__":
    try:
        # Load API token
        api_token = load_api_token("token.json")
        if not api_token:
            raise ValueError("API token is missing in token.json.")

        # Fetch anime list
        anime_list = get_anime_list(
            api_token=api_token,
            #status="watching",  # Filter for currently watching
            sort="list_score",  # Sort by score
            limit=150,           # Limit results to 4
            offset=0           # Start from the first entry
        )
        
        print("User's Anime List:")
        for anime in anime_list.get("data", []):
            title = anime["node"]["title"]
            status = anime["list_status"]["status"]
            print(f"- {title}: {status}")

    except Exception as e:
        print(f"Error: {e}")
