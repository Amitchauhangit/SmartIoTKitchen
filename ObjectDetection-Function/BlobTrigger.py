import logging
import azure.functions as func
import tempfile
import os
from detect import det

logging.basicConfig(filename='./file.log', filemode='w', level=logging.DEBUG)

app = func.FunctionApp()
containerName = "main-picture-dump"

@app.function_name(name="BlobTrigger1")
@app.blob_trigger(arg_name="fetchedblob",
                  path = containerName,
                  connection="CONNECTION_SETTING")
def test_function(fetchedblob: func.InputStream):
    file_path = fetchedblob.name
    metadata = fetchedblob.metadata

    try:
        file_name = os.path.basename(file_path)

        local_file_path = os.path.join("./images/", file_name)

        with open(local_file_path, "wb") as file:
            file.write(fetchedblob.read())

        logging.info("File downloaded to: %s", local_file_path)

        det(local_file_path,file_name, metadata)
        
        logging.info("done")
    except Exception as e:
        logging.error("Error occurred while downloading the file: %s", str(e))

   
