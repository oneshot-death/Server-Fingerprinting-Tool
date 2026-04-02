import socket
import ssl
import threading

# Service Identification Logic
def identify_service(banner):
    banner = banner.lower()

    if "apache" in banner:
        return "Apache Web Server"
    elif "nginx" in banner:
        return "Nginx Web Server"
    elif "iis" in banner:
        return "Microsoft IIS"
    elif "cloudflare" in banner:
        return "Cloudflare CDN / Reverse Proxy"
    elif "gws" in banner:
        return "Google Web Server"
    elif "ftp" in banner:
        return "FTP Server"
    elif "error" in banner:
        return "Connection Failed"
    else:
        return "Unknown Service"

# HTTP Banner Grabbing
def grab_http_banner(host, port, use_ssl=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        if use_ssl:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=host)

        sock.connect((host, port))

        request = "HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host)  #minimal HTTP req for figuring out server software
        sock.send(request.encode())

        response = sock.recv(4096).decode(errors="ignore")

        sock.close()

        return response

    except Exception as e:
        return f"Error: {e}"


# FTP Banner Grabbing
def grab_ftp_banner(host, port=21):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        sock.connect((host, port))

        banner = sock.recv(1024).decode(errors="ignore")

        sock.close()

        return banner

    except Exception as e:
        return f"Error: {e}"


# Fingerprint Target
def fingerprint_target(host):

    print(f"\nScanning {host}")

    http_banner = grab_http_banner(host, 80)
    https_banner = grab_http_banner(host, 443, use_ssl=True)
    ftp_banner = grab_ftp_banner(host)

    print("\nHTTP Banner:")
    print(host, http_banner)

    print("\nHTTPS Banner:")
    print(host, https_banner)

    print("\nFTP Banner:")
    print(host, ftp_banner)

    print(f"\nIdentified Services for {host}:")

    print("HTTP:", identify_service(http_banner))
    print("HTTPS:", identify_service(https_banner))
    print("FTP:", identify_service(ftp_banner))


# Multi-Server Testing
def scan_targets(targets):

    threads = []

    for host in targets:
        t = threading.Thread(target=fingerprint_target, args=(host,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


# Target List
targets = [
    "example.com",
    "scanme.nmap.org"
]

scan_targets(targets)
