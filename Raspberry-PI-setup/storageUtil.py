
from azure.storage.blob import BlobServiceClient
import configparser
import logging
config = configparser.ConfigParser()

config.read("config.ini")

connection_string = config.get("secrets", "connection_string")
container_name = config.get("secrets", "container_name")
username = config.get("secrets", "username")
user_details = config.get("secrets", "user_details")

metadata = {"username":username,"user_details":user_details}

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

def uploadBlob(image_path):
    try:
        with open(image_path, "rb") as filepath:
            res = container_client.upload_blob(image_path,filepath,metadata=metadata,overwrite=True)
            payload = {
            "image_url":res.url, 
            "user_details":user_details,
            "username":username
            }

    except Exception as e:
        logging.error("exception in UploadBlob %s",e)
