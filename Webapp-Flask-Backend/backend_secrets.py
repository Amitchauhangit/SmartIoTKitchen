from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

def get_secrets():
    # Authenticate with Azure Identity using default credentials
    credential = DefaultAzureCredential()
    keyvault_url = os.environ["VAULT_URL"]
    # Create a SecretClient instance
    print(keyvault_url)
    client = SecretClient(vault_url=keyvault_url, credential=credential)
    print(client)
    storage_account_name = client.get_secret("storage-account-name")
    storage_account_name = storage_account_name.value

    storage_account_key_secret = client.get_secret("storage-account-key")
    storage_account_key = storage_account_key_secret.value

    storage_container_name = client.get_secret("storage-container-name")
    storage_account_key = storage_container_name.value

    # Retrieve Cosmos DB connection string secret
    cosmosdb_connection_string_secret = client.get_secret("cosmosdb-connection-string")
    cosmosdb_connection_string = cosmosdb_connection_string_secret.value

    # Return the secrets as a dictionary
    secrets = {
        "storage_account_name": storage_account_name,
        "storage_account_key": storage_account_key,
        "storage_container_name":storage_container_name,
        "cosmosdb_connection_string": cosmosdb_connection_string
    }
    return secrets
