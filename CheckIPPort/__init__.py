import logging
import socket
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    name = req.params.get('name')
    ip = name
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
    open_ports = []
    for port in range(1, 1024):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            open_ports.append(port)
    if open_ports:
        return str(open_ports)
    else:
        print("No open ports found on " + ip_address)
