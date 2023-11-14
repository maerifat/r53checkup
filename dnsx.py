import socket

def is_private(hostname): 
    try:
        ip_address = socket.gethostbyname(hostname)
    
        private_ranges = [
            ('10.0.0.0', '10.255.255.255'),
            ('172.16.0.0', '172.31.255.255'),
            ('192.168.0.0', '192.168.255.255')
        ]
        ip_int = int.from_bytes(socket.inet_aton(ip_address), byteorder='big')
        for start, end in private_ranges:
            start_int = int.from_bytes(socket.inet_aton(start), byteorder='big')
            end_int = int.from_bytes(socket.inet_aton(end), byteorder='big')
            if start_int <= ip_int <= end_int:
                return "Private"
        return "Public"
    except:
        return "Unreachable"





