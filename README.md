# ZPC Integration for Azure Sentinel and Log Analytics Workspace

This solution requires an Azure Blob from where ZPC incidents are picked up by a Blob trigger 
and executes an Azure Function app to push data into the Log Analytics Workspace

![image](https://user-images.githubusercontent.com/60926235/222214188-6ac10b39-0e2a-4334-ab27-6444232d360b.png)

## Azure Function configuration settings

![image](https://user-images.githubusercontent.com/60926235/222214917-47f990a9-7fa6-427f-aaaa-d34c5cadbad0.png)

Basic steps:

1. Create a python Linux app
2. Upload code
3. Configure environment variables as shown in the screenshot, 
    Blob Trigger requires connection variable to the AZ Storage account, rest of the variables are self explanatory
