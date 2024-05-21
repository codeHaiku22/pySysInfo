#!/usr/bin/python
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
        internalIP = socket.gethostbyname(socket.gethostname())
        internalIP = internalIP.strip()
    except Exception as ex:
        internalIP = 'unknown'
    finally:
        return internalIP        