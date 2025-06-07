import os
from azure.storage.blob import BlobServiceClient


class AzureStorage:
    def __init__(self):
        conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
        self.client = BlobServiceClient.from_connection_string(conn_str)
