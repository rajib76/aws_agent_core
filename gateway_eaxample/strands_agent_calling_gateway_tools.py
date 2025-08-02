import boto3
from dotenv import load_dotenv
from strands import Agent
import logging
from strands.models import BedrockModel
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client
import os
import requests
import json
load_dotenv()
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


def create_streamable_http_transport(mcp_url: str, access_token: str):
    return streamablehttp_client(mcp_url, headers={"Authorization": f"Bearer {access_token}"})


def get_full_tools_list(client):
    """
    List tools w/ support for pagination
    """
    more_tools = True
    tools = []
    pagination_token = None
    while more_tools:
        tmp_tools = client.list_tools_sync(pagination_token=pagination_token)
        tools.extend(tmp_tools)
        if tmp_tools.pagination_token is None:
            more_tools = False
        else:
            more_tools = True
            pagination_token = tmp_tools.pagination_token
    return tools


def run_agent(mcp_url: str, access_token: str):
    mcp_client = MCPClient(lambda: create_streamable_http_transport(mcp_url, access_token))

    with mcp_client:
        tools = get_full_tools_list(mcp_client)
        print(f"Found the following tools: {[tool.tool_name for tool in tools]}")
        AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
        boto_session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                             region_name="us-east-1")
        model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            temperature=0.3,
            boto_session=boto_session
        )

        agent = Agent(model=model, tools=tools)
        response = agent("What is the weather in Fremont, CA?")

        print(response)


gateway_url = "https://my-gateway-pa0zbkod0e.gateway.bedrock-agentcore.us-west-2.amazonaws.com/mcp"
run_agent(gateway_url, fetch_access_token(CLIENT_ID, CLIENT_SECRET, TOKEN_URL))