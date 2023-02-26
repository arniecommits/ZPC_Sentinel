import logging
import socket
import azure.functions as func
import json
import asyncio


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    ip =""
    if(req.get_body().decode('utf8')):
        ip = req.get_body().decode('utf8')
    else:
        ip = req.params.get("ip")    
        logging.info(f'Got request body {ip}')
    if ip:
        port = check_open_ports(ip)
        port = str(asyncio.run(port))
        logging.info(f'Ports....... {port}')
        func.HttpResponse(body=f'Found the following ports open {port}',status_code=200)
        if (port):
            return func.HttpResponse(body=port,status_code=200)
        else:
            json_resp='{"ip_status":"No open ports"}'
            json_b=json.dumps(json_resp)
            return func.HttpResponse(body=json_b,status_code=200)    
    else:
        return func.HttpResponse(
             "No params passed in request",
             200
        )

async def check_open_ports(ip_address):
    open_ports = []
    for port in (22,80,443,8080,3389,1433,1521,135,445,139,53):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            open_ports.append(port)
    if open_ports:
        return str(open_ports)
    else:
        logging.info("No open ports found on " + ip_address)
        return None