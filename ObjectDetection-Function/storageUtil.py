
from azure.storage.blob import BlobServiceClient
import requests
import configparser
import logging
config = configparser.ConfigParser()

config.read("config.ini")

connection_string = config.get("secrets", "connection_string")
container_name = config.get("secrets", "container_name")
flask_api_url = config.get("secrets", "flask_api_url")

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)


def uploadBlob(image_path,image_file, metadata):
    try:
    
        with open(image_path, "rb") as file:

            res = container_client.upload_blob(image_file,file,metadata=metadata,overwrite=True)
            payload = {
            "image_url":res.url, 
            "user_details":metadata['user_details'],
            "username":metadata['username']
            }
            
        flask_add_api(payload)
    except Exception as e:
        logging.error("exception in UploadBlob %s",e)
    

def flask_add_api(payload):
    try:
        url = flask_api_url
        response = requests.post(url, json=payload)

    except Exception as e:
        logging.error("Flask-API-Error: %s",e)

    if response.status_code == 201:
        print("POST request successful.")
    else:
        print("POST request failed.")
