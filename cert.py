import ssl,socket
from cryptography import x509
from termcolor import cprint
import datetime
import re
from cryptography.hazmat.backends import default_backend
def get_cert(host,port=443):
    host=host.rstrip('.')
    try:
        socket.setdefaulttimeout(2)
        # Connect to the server and retrieve the SSL/TLS certificate
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with socket.create_connection((host, port)) as sock:
            sock.settimeout(2)
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert(binary_form=True)

        cert_pem = ssl.DER_cert_to_PEM_cert(cert)
        cert_obj = x509.load_pem_x509_certificate(cert_pem.encode(), default_backend())
        
        cn = cert_obj.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        # print(cn)
        
        san = cert_obj.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        san_entries = san.value.get_values_for_type(x509.DNSName)
        print(san_entries)
        
        san_cn_set = set(san_entries)
        san_cn_set.add(cn)
        
        if len(host.split('.')) >2:
            wildcard_host= re.sub(r'^[^.]+', '*', host)
            print(wildcard_host)
            host_list=[host,wildcard_host]
            host_set=set(host_list)
        else:
            host_set=set()
            host_set.add(host)
            
        print(host_set)
        
        if host_set not in san_cn_set:
            print("not a valid cert because of host mismatch")
            
        # print(san_cn_joint)
        
        
        
        
 
    
    except Exception as e:
        print(str(e))
                

            
get_cert("www.socialsellinguniversity.com.")