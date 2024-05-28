import socket

def get_hostname_domain_list():
    try:
        hostnameDomain = []
        hostname = socket.gethostname().strip()
        fqdn = socket.getfqdn().strip()
        domain = fqdn.replace(hostname + '.', '')
        hostnameDomain.append('hostname:' + hostname)
        hostnameDomain.append('fqdn:' + fqdn)
        hostnameDomain.append('domain:' + domain)
    except Exception as ex:
        hostnameDomain = []
        hostnameDomain.append('hostname:unknown')
        hostnameDomain.append('fqdn:unknown')
        hostnameDomain.append('domain:unknown')
    finally:
        return hostnameDomain

def get_internal_ip_address():
    try:
        sock = socket.gethostbyname(socket.gethostname())
        internalIP = sock.strip()
        if internalIP.startswith('127.0'):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(('10.255.255.255', 1))
            internalIP = sock.getsockname()[0]        
    except Exception as ex:
        internalIP = 'unknown'
    finally:
        return internalIP
