import socket
import threading
import ssl

# HTTP SERVER
def handle_http(client):
    request = client.recv(1024)

    response = """HTTP/1.1 200 OK
Server: Apache/2.4.57
Content-Type: text/html

<html><body><h1>Test Server</h1></body></html>
"""

    client.send(response.encode())
    client.close()


def http_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 8080))
    s.listen(5)

    print("HTTP server running on port 8080")

    while True:
        client, addr = s.accept()
        threading.Thread(target=handle_http, args=(client,)).start()


# FTP BANNER SERVER
def handle_ftp(client):
    banner = "220 vsFTPd 3.0.3 FTP Server Ready\r\n"
    client.send(banner.encode())
    client.close()


def ftp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 2121))
    s.listen(5)

    print("FTP server running on port 2121")

    while True:
        client, addr = s.accept()
        threading.Thread(target=handle_ftp, args=(client,)).start()


# HTTPS SERVER
def handle_https(client):
    request = client.recv(1024)

    response = """HTTP/1.1 200 OK
Server: nginx/1.18
Content-Type: text/html

<html><body><h1>Secure Server</h1></body></html>
"""

    client.send(response.encode())
    client.close()


def https_server():

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("cert.pem", "key.pem")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 8443))
    s.listen(5)

    print("HTTPS server running on port 8443")

    while True:
        client, addr = s.accept()
        ssl_client = context.wrap_socket(client, server_side=True)

        threading.Thread(target=handle_https, args=(ssl_client,)).start()


# START ALL SERVICES
threading.Thread(target=http_server).start()
threading.Thread(target=ftp_server).start()
threading.Thread(target=https_server).start()

print("Test servers started.")