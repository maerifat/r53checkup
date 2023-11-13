import ssl
import socket
import datetime
def check_certificate(host, port=443):
    # Connect to the server and retrieve the SSL/TLS certificate
    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            cert = ssock.getpeercert()
            cipher = ssock.cipher()

    # Check validity period
    current_date = datetime.datetime.utcnow()

    not_before = datetime.datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z")
    not_after = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")


    

    print(cipher)


    if not_before <= current_date <= not_after:
        print("Certificate is currently valid.")
    else:
        print("Certificate is not currently valid.")

    # Check CN and SAN
    cn = cert['subject'][0][0][1]
    san = [x[1] for x in cert.get('subjectAltName', []) if x[0] == 'DNS']

    if host == cn or host in san:
        print(f"CN and SAN match the host: {host}")
    else:
        print(f"CN or SAN does not match the host: {host}")

# Example usage
host_to_check = "facebook.com"
port_to_check = 443

check_certificate(host_to_check, port_to_check)
