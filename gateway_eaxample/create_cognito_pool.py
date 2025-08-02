from bedrock_agentcore_starter_toolkit.operations.gateway import GatewayClient

client = GatewayClient(region_name="us-west-2")
cognito_result = client.create_oauth_authorizer_with_cognito("my-gateway")

print(cognito_result)