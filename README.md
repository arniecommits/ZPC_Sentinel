# ZPC Integration for Azure Sentinel and Log Analytics Workspace

This solution requires an Azure Blob from where ZPC incidents are picked up by a Blob trigger 
and executes an Azure Function app to push data into the Log Analytics Workspace

![image](https://user-images.githubusercontent.com/60926235/222214188-6ac10b39-0e2a-4334-ab27-6444232d360b.png)

## Azure Function configuration settings

![image](https://user-images.githubusercontent.com/60926235/222214917-47f990a9-7fa6-427f-aaaa-d34c5cadbad0.png)

Basic steps:

1. Create a python Linux app
2. Upload the code by creating a workspace in your local machine and leveraging VScode integrations
3. Assign a managed identity to the function ensure the service principal has read access to azure blobs and write access to log analytics workspace and sentinel
4. Configure a Log Analytics Workspace and obtain workspace id, rg info etc optional map this into Microsoft Sentinel for Incident Management
5. Configure environment variables as shown in the screenshot, 
    Blob Trigger requires connection variable to the AZ Storage account, rest of the variables are self explanatory

## Sentinel SOAR Integration

![image](https://user-images.githubusercontent.com/60926235/222216327-2b7f4b55-6482-41cc-93d2-b2a71a29c5ed.png)

Eg. Detection Rule for Sentinel ![image](https://user-images.githubusercontent.com/60926235/222216625-ddc4e3d9-613c-4cf2-a763-3bf219b23840.png)

ZscalerPosture_CL
| where type_s != "IaC"
    and app_s == "AZURE"
    and signature_category_s == "External Exposure"   
| extend resourceGroup = split(src_id_s,'/',4)
| extend subscriptionId = split(src_id_s,'/',2)
| project src_id_s, src_name_s, resourceGroup,subscriptionId,signature_category_s
