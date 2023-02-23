import logging
import json
import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient, BlobClient



def main(myblob: func.InputStream):
    blob_bytes = myblob.read()
    object_contents = blob_bytes.decode('utf-8')
    for line in object_contents.splitlines():
            json_content = json.loads(line)
            logging.info(json_content)
    