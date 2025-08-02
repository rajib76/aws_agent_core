import requests
import json

from strands import Agent
from strands.models import BedrockModel

CLIENT_ID = "5l697o18dhjr96cdu6hng1mn7j"
CLIENT_SECRET = "8q1cblllrdf6dmetcildegiua1r7ovpviqc100qub0qbrl9apfm"
TOKEN_URL = "https://agentcore-1e2056ef.auth.us-west-2.amazoncognito.com/oauth2/token"


def fetch_access_token(client_id, client_secret, token_url):
    response = requests.post(
        token_url,
        data="grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}".format(
            client_id=client_id, client_secret=client_secret),
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    return response.json()['access_token']


def list_tools(gateway_url, access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "jsonrpc": "2.0",
        "id": "list-tools-request",
        "method": "tools/list"
    }

    response = requests.post(gateway_url, headers=headers, json=payload)
    return response.json()


# Example usage
gateway_url = "https://my-gateway-pa0zbkod0e.gateway.bedrock-agentcore.us-west-2.amazonaws.com/mcp"
access_token = fetch_access_token(CLIENT_ID, CLIENT_SECRET, TOKEN_URL)
tools = list_tools(gateway_url, access_token)
print(json.dumps(tools, indent=2))

