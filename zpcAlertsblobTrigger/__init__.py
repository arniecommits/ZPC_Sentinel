import logging
import json
import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient, BlobClient
import time
import hmac
import hashlib
import base64
import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.loganalytics import LogAnalyticsManagementClient
import os
az_workspace_id = '8926b370-797c-4914-9ab1-1dfcb1808976'
az_workspace_name = 'ARNAB-LAB'
log_type = 'ZscalerPosture'
az_sub_id ='d3064f82-30cf-4e0e-b27f-e6c5fddbc9b2'
az_rg_name = 'rg-arnab-lab'
api_version = '2016-04-01'


def main(myblob: func.InputStream):
    shared_key = get_shared_key()
    blob_bytes = myblob.read()
    object_contents = blob_bytes.decode('utf-8')
    for line in object_contents.splitlines():
            json_content = json.loads(line)
            send_aw(json_content,shared_key)
            #logging.info(json_content)

def get_shared_key ():
    client = LogAnalyticsManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=az_sub_id,
    )

    response = client.shared_keys.get_shared_keys(
        resource_group_name=az_rg_name,
        workspace_name=az_workspace_name
    )
    logging.info(f'Shared Key :{response}')
    return response

def send_aw(json_data,key):
    
    endpoint = f'https://{az_workspace_id}.ods.opinsights.azure.com/api/logs?api-version={api_version}'
    timestamp = str(int(time.time()))
    string_to_sign = f'{timestamp}{json_data}'
    signature = base64.b64encode(hmac.new(base64.b64decode(key), msg=string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()).decode()
    headers = {
        'Content-Type': 'application/json',
        'Log-Type': log_type,
        'Authorization': f'SharedKey {az_workspace_id}:{signature}',
        'x-ms-date': timestamp,
    }
    response = requests.post(endpoint, data=json_data, headers=headers)
    if response.status_code == 200:
        logging.info('Data sent successfully to Log Analytics workspace')
    else:
        logging.error(f'Error sending data to Log Analytics workspace: {response.status_code} - {response.content}')

