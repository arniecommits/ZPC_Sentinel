import json
import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient, BlobClient
import datetime
import hmac
import hashlib
import base64
import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.loganalytics import LogAnalyticsManagementClient
import os
az_workspace_id = os.environ['az_workspace_id']
az_workspace_name = os.environ['az_workspace_name']
log_type = os.environ['log_type']
az_sub_id =os.environ['az_sub_id']
az_rg_name = os.environ['az_rg_name']





def main(myblob: func.InputStream):
    shared_key = get_shared_key()
    blob_bytes = myblob.read()
    object_contents = blob_bytes.decode('utf-8')
    dict_list = []
    for line in object_contents.splitlines():
            json_content = json.loads(line)
            dict_list.append(json_content)
    json_data_all = json.dumps(dict_list)        
    logging.info(f'Following events are being pushed to logs: {json_data_all}')
    send_aw(az_workspace_id,shared_key,json_data_all,log_type)
            

def get_shared_key ():
    client = LogAnalyticsManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=az_sub_id,
    )

    response = client.shared_keys.get_shared_keys(
        resource_group_name=az_rg_name,
        workspace_name=az_workspace_name
    )
    response = response.primary_shared_key
    return response

def build_signature(WORKSPACE_ID, WORKSPACE_SHARED_KEY, date, content_length, method, content_type, resource):
    x_headers = 'x-ms-date:' + date
    string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
    bytes_to_hash = bytes(string_to_hash, encoding="utf-8") 
    decoded_key = base64.b64decode(WORKSPACE_SHARED_KEY)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
    authorization = f"SharedKey {WORKSPACE_ID}:{encoded_hash}"
    return authorization

def send_aw(WORKSPACE_ID, WORKSPACE_SHARED_KEY, body, LOG_TYPE):
    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)
    signature = build_signature(WORKSPACE_ID, WORKSPACE_SHARED_KEY, rfc1123date, content_length, method, content_type, resource)
    uri = 'https://' + WORKSPACE_ID + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'

    headers = {
        'content-type': content_type,
        'Authorization': signature,
        'Log-Type': LOG_TYPE,
        'x-ms-date': rfc1123date
    }

    logging.info(f'Sending {content_length} bytes')
    response = requests.post(uri,data=body, headers=headers)
    if (response.status_code >= 200 and response.status_code <= 299):
        logging.info('Sent data successfully to Log Analytics Workspace')
        return True
    else:
        logging.error(f'Response code: {response.status_code} Response : {response.text}')
    
    
