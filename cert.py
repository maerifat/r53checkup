import ssl
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import re
from datetime import datetime

def get_cert(host, port=443):
    host = host.rstrip('.')
    try:
        
        # Connect to the server and retrieve the SSL/TLS certificate
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection((host, port)) as sock:
            
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert(binary_form=True)
                cipher = ssock.cipher()
                cipher_name = cipher[0]

        cert_pem = ssl.DER_cert_to_PEM_cert(cert)
        cert_obj = x509.load_pem_x509_certificate(cert_pem.encode(), default_backend())

        cn = cert_obj.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        
        san_raw = cert_obj.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        san = san_raw.value.get_values_for_type(x509.DNSName)
        
        # Add the CN to the SAN entries for comparison
        cn_san_union=[]
        cn_san_union.append(cn)
        
        cn_san_union.extend(san)
        
        
        
        # Check if the provided host matches any SAN or CN entry
        if len(host.split('.')) > 2:
            wildcard_host = re.sub(r'^[^.]+', '*', host)
            host_list = [host, wildcard_host]
        else:
            host_list = [host]

        host_set = set(host_list)

        # Check for intersection between host_set and san_entries
        if host_set.intersection(set(cn_san_union)):
            validation="passed"
        else:
            validation="Failed"

            # Get issue and expiry dates
        issue_date = cert_obj.not_valid_before
        expiry_date = cert_obj.not_valid_after
        print(validation)
        print("Issue Date:", issue_date)
        print("Expiry Date:", expiry_date)

    except Exception as e:
        print(str(e))

get_cert("pgextract.emr.gdpr-stg.demandbase.com")
