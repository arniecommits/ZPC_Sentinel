import logging
import nmap
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    ip = req.params.get('ipAddr')
    if ip:
        port = check_open_ports(ip)
        if port:
            return func.HttpResponse(body=f'{port}',status_code=200)
        else:
            return func.HttpResponse(body=f'No open ports detected on {ip}',status_code=404)    
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
def check_open_ports(ip_address):
    nm = nmap.PortScanner()
    result = nm.scan(ip_address, arguments="-p 1-1024")
    for port in result["scan"][ip_address]["tcp"]:
        if result["scan"][ip_address]["tcp"][port]["state"] == "open":
            logging.info("Port " + port + " is open on " + ip_address)
            return port
        else:
            exit    