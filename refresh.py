import json
import requests
from dotenv import load_dotenv
import os
# Load environment variables from the .env file
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")  # May be None if not set
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_BASE_URL = os.getenv("AUTH_BASE_URL")
TOKEN_URL = os.getenv("TOKEN_URL")


def refresh_access_token(refresh_token):
    """
    Refresh the access token using the refresh token.
    """
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,  # Include only if your app is "Web"
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(TOKEN_URL, data=payload, headers=headers)
    return response.json()

# Step 1: File to read
input_file = "output.json"

# Step 2: Read and parse the JSON file
try:
    with open(input_file, "r") as infile:
        data = json.load(infile)  # Parse JSON into a Python dictionary

    # Step 3: Display the parsed data
    print("Parsed JSON data:")
    print(data)

    refreshed_tokens = refresh_access_token(data["refresh_token"])
    print("Refreshed Tokens:")
    print(refreshed_tokens)

except FileNotFoundError:
    print(f"Error: The file {input_file} does not exist.")
except json.JSONDecodeError as e:
    print(f"Error: Failed to parse JSON file. {e}")