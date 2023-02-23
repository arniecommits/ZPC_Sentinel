import logging
import json
import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient, BlobClient



def main(myblob: func.InputStream):
    blob_bytes = myblob.read()
    blob_string = blob_bytes.decode('utf-8')
    data = json.loads(blob_string)
    logging.info(f"Got data: {data}")