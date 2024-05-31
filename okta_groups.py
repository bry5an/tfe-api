from okta.client import Client as OktaClient
import asyncio
import os
import requests

def get_access_key():
    # Get environment variables
    client_id = os.getenv("HCP_CLIENT_ID")
    client_secret = os.getenv("HCP_CLIENT_SECRET")

    # Define the data and headers
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "audience": "https://api.hashicorp.cloud"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Make the request
    response = requests.post("https://auth.idp.hashicorp.com/oauth2/token", data=data, headers=headers)

    # Get the JSON response
    json_response = response.json()
    return json_response['access_key']

async def get_groups(client):
    # Fetch all groups
    groups, _, _ = await client.list_groups()
    return groups

async def main():
    access_key = get_access_key()

    # Initialize Okta client
    config = {
        "orgUrl": os.getenv("OKTA_ORG_URL"),
        "token": os.getenv("OKTA_API_TOKEN")
    }
    client = OktaClient(config)

    groups = await get_groups(client)

# Run the script
asyncio.run(main())