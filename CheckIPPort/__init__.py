import logging
import socket
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    ip = req.get_body().decode('utf8')

    logging.info(f'Got request body {ip}')
    if ip:
        port = check_open_ports(ip)
        if port:
            return func.HttpResponse(body=f'{port}',status_code=200)
        else:
            return func.HttpResponse(body=f'{"status":"No open ports"}',status_code=200)    
    else:
        return func.HttpResponse(
             f"Request body {ip}",
             status_code=200
        )

def check_open_ports(ip_address):
    open_ports = []
    for port in (22,80,443,8080,3389,1433,1521,135,445,139,53):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            open_ports.append(port)
    if open_ports:
        return str(open_ports)
    else:
        print("No open ports found on " + ip_address)
