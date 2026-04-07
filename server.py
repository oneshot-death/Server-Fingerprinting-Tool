import socket
import threading
import ssl


# HTTP SERVER
def handle_http(client):
    try:
        client.settimeout(5)
        client.recv(1024)  # Read and discard the request

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Server: Apache/2.4.57\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            "<html><body><h1>Test Server</h1></body></html>"
        )

        client.send(response.encode())
    except Exception as e:
        print(f"[HTTP] Client handler error: {e}")
    finally:
        client.close()


def http_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Avoid "Address already in use" on restart
    s.bind(("0.0.0.0", 8080))
    s.listen(5)

    print("HTTP server running on port 8080")

    while True:
        client, addr = s.accept()
        threading.Thread(target=handle_http, args=(client,), daemon=True).start()


# FTP BANNER SERVER
def handle_ftp(client):
    try:
        banner = "220 vsFTPd 3.0.3 FTP Server Ready\r\n"
        client.send(banner.encode())
    except Exception as e:
        print(f"[FTP] Client handler error: {e}")
    finally:
        client.close()


def ftp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Avoid "Address already in use" on restart
    s.bind(("0.0.0.0", 2121))
    s.listen(5)

    print("FTP server running on port 2121")

    while True:
        client, addr = s.accept()
        threading.Thread(target=handle_ftp, args=(client,), daemon=True).start()


# HTTPS SERVER
def handle_https(client):
    try:
        client.settimeout(5)
        client.recv(1024)  # Read and discard the request

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Server: nginx/1.18\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            "<html><body><h1>Secure Server</h1></body></html>"
        )

        client.send(response.encode())
    except Exception as e:
        print(f"[HTTPS] Client handler error: {e}")
    finally:
        client.close()


def https_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("cert.pem", "key.pem")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Avoid "Address already in use" on restart
    s.bind(("0.0.0.0", 8443))
    s.listen(5)

    print("HTTPS server running on port 8443")

    while True:
        client, addr = s.accept()
        try:
            # Wrap each accepted socket individually so an SSL handshake
            # failure from one client doesn't crash the entire server loop
            ssl_client = context.wrap_socket(client, server_side=True)
        except ssl.SSLError as e:
            print(f"[HTTPS] SSL handshake failed for {addr}: {e}")
            client.close()
            continue

        threading.Thread(target=handle_https, args=(ssl_client,), daemon=True).start()


if __name__ == "__main__":
    # START ALL SERVICES
    threading.Thread(target=http_server, daemon=True).start()
    threading.Thread(target=ftp_server, daemon=True).start()
    threading.Thread(target=https_server, daemon=True).start()

    print("Test servers started.")

    # Keep the main thread alive so daemon threads keep running
    threading.Event().wait()