import secrets
import requests
import webbrowser
import json
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
# Configuration
CLIENT_ID = "bdb6a93195d6ef2f4b7b80e7865a6d33"
CLIENT_SECRET = "b4026adef2807ca6479ae1a49c0ba02066d2d6d29c1154b407f08271b2b8ba1c"  # Optional, only if your app is a "Web" type
REDIRECT_URI = "http://localhost/oauth"  # Registered redirect URI
AUTH_BASE_URL = "https://myanimelist.net/v1/oauth2/authorize"
TOKEN_URL = "https://myanimelist.net/v1/oauth2/token"

def get_new_code_verifier():
    """
    Generate a PKCE Code Verifier and Code Challenge.
    """
    token = secrets.token_urlsafe(100)
    return token[:128]

def get_authorization_url(client_id, code_challenge, state=None, redirect_uri=None):
    """
    Build the authorization URL.
    """
    params = {
        "response_type": "code",
        "client_id": client_id,
        "code_challenge": code_challenge,
        "state": state or "random_state",
        "redirect_uri": redirect_uri,
    }
    # Construct URL
    url = f"{AUTH_BASE_URL}?" + "&".join(f"{key}={value}" for key, value in params.items() if value)
    return url

def get_access_token(auth_code, code_verifier):
    """
    Exchange the authorization code for an access token.
    """
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,  # Include only if your app is "Web"
        "code": auth_code,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(TOKEN_URL, data=payload, headers=headers)
    return response.json()

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

# Step 1: Generate PKCE Code Verifier and Challenge
code_verifier = get_new_code_verifier()
code_challenge = code_verifier  # For MAL, Code Challenge equals Code Verifier

# Step 2: Get Authorization URL and redirect user
authorization_url = get_authorization_url(CLIENT_ID, code_challenge, redirect_uri=REDIRECT_URI)
print("Go to the following URL to authorize the app:")
print(authorization_url)
webbrowser.open(authorization_url)

# Step 3: User provides the Authorization Code after redirection
auth_code = input("Enter the authorization code from the URL: ")

# Step 4: Exchange the Authorization Code for an Access Token
tokens = get_access_token(auth_code, code_verifier)
print("Access Token and Refresh Token:")
print(tokens)

#output to file
output_file = "output.json"

with open(output_file, "w") as outfile:
    json.dump(tokens, outfile, indent=4)