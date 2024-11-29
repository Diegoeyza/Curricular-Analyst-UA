import os
import requests

# Load environment variables
DAP_API_URL = os.getenv('DAP_API_URL', 'https://api-gateway.instructure.com')
DAP_CLIENT_ID = os.getenv('DAP_CLIENT_ID')
DAP_CLIENT_SECRET = os.getenv('DAP_CLIENT_SECRET')

if not all([DAP_CLIENT_ID, DAP_CLIENT_SECRET]):
    raise ValueError("Client ID and Client Secret must be set.")

def get_access_token(base_url, client_id, client_secret):
    url = f"{base_url}/oauth/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an error for bad status codes

    return response.json()['access_token']

def list_tables(base_url, access_token, namespace):
    url = f"{base_url}/v1/{namespace}/tables"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes

    return response.json()

# Obtain access token
access_token = get_access_token(DAP_API_URL, DAP_CLIENT_ID, DAP_CLIENT_SECRET)

# List tables in the 'ingenieria' namespace
tables = list_tables(DAP_API_URL, access_token, 'ingenieria')
for table in tables:
    print(table)
