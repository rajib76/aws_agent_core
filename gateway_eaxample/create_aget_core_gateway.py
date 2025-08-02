from bedrock_agentcore_starter_toolkit.operations.gateway import GatewayClient

client = GatewayClient(region_name="us-west-2")

cognito_result={'authorizer_config': {'customJWTAuthorizer': {'allowedClients': ['5l697o18dhjr96cdu6hng1mn7j'], 'discoveryUrl': 'https://cognito-idp.us-west-2.amazonaws.com/us-west-2_BBJrKZ8YS/.well-known/openid-configuration'}}, 'client_info': {'client_id': '5l697o18dhjr96cdu6hng1mn7j', 'client_secret': '8q1cblllrdf6dmetcildegiua1r7ovpviqc100qub0qbrl9apfm', 'user_pool_id': 'us-west-2_BBJrKZ8YS', 'token_endpoint': 'https://agentcore-1e2056ef.auth.us-west-2.amazoncognito.com/oauth2/token', 'scope': 'my-gateway/invoke', 'domain_prefix': 'agentcore-1e2056ef'}}

gateway = client.create_mcp_gateway(
    name="my-gateway", # the name of the Gateway - if you don't set one, one will be generated.
    role_arn=None, # the role arn that the Gateway will use - if you don't set one, one will be created.
    authorizer_config=cognito_result["authorizer_config"], # the OAuth authorizer details for authorizing callers to your Gateway (MCP only supports OAuth).
    enable_semantic_search=True, # enable semantic search.
)
print(gateway)

# create a lambda target.
lambda_target = client.create_mcp_gateway_target(
    gateway=gateway,
    name=None, # the name of the Target - if you don't set one, one will be generated.
    target_type="lambda", # the type of the Target - you will see other target types later in the tutorial.
    target_payload=None, # the target details - set this to define your own lambda if you pre-created one. Otherwise leave this None and one will be created for you.
    credentials=None,# required to ocnnect to apis
)


# print(f"MCP Endpoint: {gateway.get_mcp_url()}")
# print(f"OAuth Credentials:")
# print(f"  Client ID: {cognito_result['client_info']['client_id']}")
# print(f"  Scope: {cognito_result['client_info']['scope']}")
