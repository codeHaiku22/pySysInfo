#!/usr/bin/python3

import psi_file as pfl
import psi_formatting as pfmt
import psi_network as pnet
import psi_shell as psh
import psi_system as psys
import psi_web as pweb
import sys

def main():
    blnWeather = False
    if (len(sys.argv) > 1):
        if ((sys.argv[1] == '-h') or (sys.argv[1] == '--help')):
            pfmt.print_help()
            exit()        
        if ((sys.argv[1] == '-w' ) or (sys.argv[1] == '--weather')) and (len(sys.argv) == 4):
            location = sys.argv[2]
            if (sys.argv[3] == '1' or sys.argv[3] == '2' or sys.argv[3] == '3'): 
                detail = int(sys.argv[3])
                weather = pweb.get_forecast(location, detail)
                if (weather == 'unknown'): weather = psh.get_forecast(location, detail)
                blnWeather = True 
    rightNow = psys.get_current_datetime()
    hostNameDomain = pnet.get_hostname_domain_list()
    hostName = hostNameDomain[0].split(':')[1]
    fqdn = hostNameDomain[1].split(':')[1]
    domain = hostNameDomain[2].split(':')[1]
    architectures = psys.get_architecture_list()
    bit = architectures[0].split(':')[1]
    executable = architectures[1].split(':')[1]
    machine = architectures[2].split(':')[1]
    processor = architectures[3].split(':')[1]
    architecture = bit + ' ' + executable +  ' (' + machine + ')'
    distro = pfl.get_distribution()
    kernelInfo = psys.get_kernel_info_list()
    kernel = kernelInfo[0].split(':')[1]
    microsoftWSL = (kernelInfo[1].split(':')[1] == 'True')
    if microsoftWSL: distro += ' (WSL)' 
    cpus = pfl.get_cpu_list()
    cpuLoad = pfl.get_load_average()
    gpus = psh.get_gpu_list(microsoftWSL)
    internalIP = pnet.get_internal_ip_address()
    externalIP = pweb.get_external_ip_address()
    if (externalIP == 'unknown'): externalIP = psh.get_external_ip_address() 
    upTime = pfl.get_uptime()
    cpuPercentUsed = pfl.get_cpu_percent()
    ramPercentUsed, ramUsage = pfl.get_ram_usage_list()
    ramAmountUsed = ramUsage[0].split(':')[1]
    ramAmountTotal = ramUsage[1].split(':')[1]
    diskUsage = pfl.get_disk_usage_list(microsoftWSL)
    maxKeyLen = 12  #"Architecture"
    maxUsgKeyLen = 0
    maxFSLen = 0
    for disk in diskUsage:
        diskDevice = disk[0].split(':')[1]
        diskFileSystem = disk[2].split(':')[1]
        if (len(diskDevice) + len('Disk []') > maxUsgKeyLen): maxUsgKeyLen = len(diskDevice) + len('Disk []')
        if (len(diskFileSystem) > maxFSLen): maxFSLen = len(diskFileSystem)
    print('')
    if blnWeather:
        pfmt.print_output(type='heading', output='Weather')        
        print(weather)
    pfmt.print_output(type='heading', output='Date & Time')
    pfmt.print_output(type='simple', output=rightNow)
    print('')
    pfmt.print_output(type='heading', output='System')
    pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='Hostname', value=hostName)
    pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='Domain', value=domain)
    pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='FQDN', value=fqdn)
    pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='Architecture', value=architecture)
    pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='Distro', value=distro)
    pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='Kernel', value=kernel)
    i = 0
    for cpu in cpus:
        if (len(cpus) > 1):
            pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='CPU' + ' ' + str(i), value=cpu)
            i += 1
        else:
            pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='CPU', value=cpu)
    pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='CPU Load', value=cpuLoad)            
    i = 0
    for gpu in gpus:
        if (len(gpus) > 1):
            pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='GPU' + ' ' + str(i), value=gpu)
            i += 1
        else:
            pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='GPU', value=gpu)  
    pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='Internal IP', value=internalIP)               
    pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='Public IP', value=externalIP) 
    pfmt.print_output(type='keyvalue', keyLen=maxKeyLen, key='Uptime', value=upTime) 
    print('')
    pfmt.print_output(type='heading', output='Usage')
    pfmt.print_output(type='keyusage', keyLen=maxUsgKeyLen, key='CPU', usagePct=cpuPercentUsed) 
    pfmt.print_output(type='keyusage', keyLen=maxUsgKeyLen, key='Memory', usagePct=ramPercentUsed, usageAmt=ramAmountUsed, usageTtl=ramAmountTotal) 
    for disk in diskUsage:
        diskDevice = disk[0].split(':')[1]
        diskMount = disk[1].split(':')[1]
        diskFileSystem = disk[2].split(':')[1]
        diskAmountUsed = disk[3].split(':')[1]
        diskAmountTotal = disk[4].split(':')[1]
        diskPercentUsed = int(disk[5].split(':')[1])
        diskEntry = ('Disk [' + diskDevice + ']').ljust(maxUsgKeyLen)
        pfmt.print_output(type='keyusage', keyLen=maxUsgKeyLen, key=diskEntry, usagePct=diskPercentUsed, usageAmt=diskAmountUsed, usageTtl=diskAmountTotal, fsLen=maxFSLen, fs=diskFileSystem, mount=diskMount) 
    print('')
    
if __name__ == "__main__":
    main()
