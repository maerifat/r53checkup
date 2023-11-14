import ssl,socket
from cryptography import x509
from termcolor import cprint
import datetime
from cryptography.hazmat.backends import default_backend
def get_cert(host,port=443):
    try:
        socket.setdefaulttimeout(2)
        # Connect to the server and retrieve the SSL/TLS certificate
        context = ssl.create_default_context()
        with socket.create_connection((host, port)) as sock:
            sock.settimeout(2)
            with context.wrap_socket(sock, server_hostname=host,) as ssock:
                cert = ssock.getpeercert(binary_form=False)
                cipher = ssock.cipher()[0]

        if cert:
            current_date = datetime.datetime.utcnow()
            not_before = datetime.datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z")
            not_after = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
            cn = cert['subject'][0][0][1]
            san = ' , '.join([x[1] for x in cert.get('subjectAltName', []) if x[0] == 'DNS'])
            print(cipher)
            print(san)

    # except ssl.SSLError as e:
    #     print("SSL Error:", e)
    #     print("Cipher:", cipher)
    #     print("san: ", san )

    except ssl.SSLCertVerificationError as p:
        cprint("There is mismatch1","red",None)
        print(p)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert(binary_form=True)
        print(cert)

        cert_pem = ssl.DER_cert_to_PEM_cert(cert)
        print(cert_pem)
        cert_obj = x509.load_pem_x509_certificate(cert_pem.encode(), default_backend())
        print(cert_obj)
        cert_bytes = cert_obj.public_bytes(encoding=serialization.Encoding.PEM)
        san = cert_obj.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        print(san)
        san_entries = san.value.get_values_for_type(x509.DNSName)
        print(san_entries)
                

            
get_cert("www.trust.insideview.com")