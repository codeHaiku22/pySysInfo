import datetime
import os
import shutil

def get_cpu_list():
    try:
        file = open('/proc/cpuinfo', 'r')
        cpuInfo = []
        cpu = ''
        speed = ''
        cores = ''
        entry = ''
        for line in file:
            if (line.split(':')[0].strip().lower() == 'processor'):
                if (cpu != ''):
                    entry = (cpu + speed + cores).strip()
                    if (entry not in cpuInfo): cpuInfo.append(entry)
                    cpu = ''
                    speed = ''
                    cores = ''
            if (line.split(':')[0].strip().lower() == 'model name'): cpu = line.split(':')[1].strip()
            if ('hz' in line.split(':')[0].strip().lower()) and ('hz' not in cpu.lower()): 
                unit = line.split(':')[0].strip().split()[1].lower()
                cycles = float(line.split(':')[1].strip())
                if (cycles >= 1000):
                    cycles = round((cycles/1000), 2)
                    if (unit == 'hz'):
                        unit = 'KHz'
                    elif (unit == 'khz'):
                        unit = 'MHz'
                    elif (unit == 'mhz'):
                        unit = 'GHz'
                    elif (unit == 'ghz'):
                        unit = 'THz'
                    elif (unit == 'thz'):
                        unit = 'PHz'
                speed = ' @ ' + str(cycles) + unit 
            if (line.split(':')[0].strip().lower() == 'cpu cores'):
                cores = ' (' + line.split(':')[1].strip() + ' core)' if (line.split(':')[1].strip() == 1) else ' (' + line.split(':')[1].strip() + ' cores)'
        if (cpu != ''):
            entry = (cpu + speed + cores).strip()
            if (entry not in cpuInfo): cpuInfo.append(entry)
        cpuInfo.sort()
    except Exception as ex:
        cpuInfo = []
        cpuInfo.append('unknown')
    finally:
        file.close()
        return cpuInfo

def get_cpu_percent():
    try:
        cpuStats = ''
        with open('/proc/stat', 'r') as file:
            cpuStats = file.readline().split()
        user = int(cpuStats[1])
        system = int(cpuStats[3])
        idle = int(cpuStats[4])
        cpuPercent = int(((user + system) * 100) / (user + system + idle))
    except Exception as ex:
        cpuPercent = -1
    finally:
        return cpuPercent

def get_disk_usage_list(microsoftWSL):
    try:
        diskUsage = []
        #with open('/etc/mtab', 'r') as file:
        with open('/proc/mounts', 'r') as file:
            allmounts = file.readlines()
        diskmounts = list(filter(lambda entry: entry.startswith('/dev/'), allmounts))
        for dm in diskmounts:
            dskusg = [] 
            dev = dm.split(' ')[0].strip()
            mntpt = dm.split(' ')[1].strip()
            fs = dm.split(' ')[2].strip()
            if (microsoftWSL and mntpt.startswith('/mnt/wsl')): continue
            shutil.disk_usage(mntpt)       # x= usage(total=1081101176832, used=4672487424, free=1021436334080) | x.free = 1021436334080 etc. ...
            dskUsd = shutil.disk_usage(mntpt).used
            dskTtl = shutil.disk_usage(mntpt).total
            dskPrcnt = int((dskUsd / dskTtl) * 100)
            if (dskTtl > 1024**5):
                coefficient = 1024**5
                unit = 'PB'
            elif (dskTtl > 1024**4):
                coefficient = 1024**4
                unit = 'TB'
            elif (dskTtl > 1024**3):
                coefficient = 1024**3
                unit = 'GB'
            elif (dskTtl > 1024**2):
                coefficient = 1024**2
                unit = 'MB'
            elif (dskTtl > 1024**1):
                coefficient = 1024**1
                unit = 'KB'
            else:
                coefficient = 1
                unit = 'B'
            dskUsd /= coefficient
            dskTtl /= coefficient
            dskusg.append('device:' + dev)
            dskusg.append('mount:' + mntpt)
            dskusg.append('filesystem:' + fs)
            dskusg.append('amt_used:' + '{0:.1f}'.format(dskUsd) + ' ' + unit)
            dskusg.append('amt_total:' + '{0:.1f}'.format(dskTtl) + ' ' + unit)
            dskusg.append('pct_used:' + str(dskPrcnt))
            diskUsage.append(dskusg)
        diskUsage.sort()
    except Exception as ex:
        diskUsage = []
        dskusg.append('device:unknown')
        dskusg.append('mount:/dev/null')
        dskusg.append('filesystem:unknown')
        dskusg.append('amt_used:' + '{0:.1f}'.format(-1) + ' ' + 'B')
        dskusg.append('amt_total:' + '{0:.1f}'.format(-1) + ' ' + 'B')
        dskusg.append('pct_used:' + str(-1))        
    finally:
        return diskUsage

def get_distribution():
    try:
       #platform.freedesktop_os_release()
        distroInfo = []
        for object in os.scandir('/etc'):
            if ('release' in object.name) and (object.is_file() or object.is_symlink()):
                with open(os.path.join('/etc', object.name), 'r') as file:
                    distroInfo += file.readlines()
            else:
                continue
        distroInfo = [item.replace('\n', '') for item in distroInfo]
        distroInfo = [item.replace('"', '') for item in distroInfo]
        pnIndex = [item.find('PRETTY_NAME') for item in distroInfo]
        ddIndex = [item.find('DISTRIB_DESCRIPTION') for item in distroInfo]
        distribution = ''
        if (0 in pnIndex): distribution = distroInfo[pnIndex.index(0)].split('=')[1]
        elif (0 in ddIndex): distribution = distroInfo[ddIndex.index(0)].split('=')[1]
        else:
            distrib_id = ''
            distrib_release = ''
            name = ''
            version_id = ''
            version = ''
            for entry in distroInfo:
                if (entry.split('=')[0].lower() == 'distrib_id'):
                    distrib_id = entry.split('=')[1]
                elif (entry.split('=')[0].lower() == 'distrib_release'):
                    distrib_release=entry.split('=')[1]
                elif (entry.split('=')[0].lower() == 'name'):
                    name = entry.split('=')[1]
                elif (entry.split('=')[0].lower() == 'version_id'):
                    version_id=entry.split('=')[1]
                elif (entry.split('=')[0].lower() == 'version'):
                    version=entry.split('=')[1]     
            if (len(name) > 0):
                distribution += name
                if (len(version) > 0):
                    distribution += ' ' + version
                elif (len(version_id) > 0):
                    distribution += ' ' + version_id
            elif (len(distrib_id) > 0):
                distribution += distrib_id
                if (len(distrib_release) > 0):
                    distribution += ' ' + distrib_release
            else:
                distribution = 'unknown'
        distribution = distribution.strip()
    except Exception as ex:
        distribution = 'unknown'
    finally:
        return distribution

def get_load_average():
    try:
        loadAverage = ''
        with open('/proc/loadavg', 'r') as file:
            loadAverage = ', '.join(file.readline().split()[0:3])
            loadAverage = loadAverage.strip()
    except Exception as ex:
        loadAverage = '-1, -1, -1'
    finally:
        return loadAverage

def get_ram_usage_list():
    try:
        ramUsage = []
        memInfo = []
        with open('/proc/meminfo', 'r') as file:
            memInfo = file.readlines()
        memInfo = [item.replace('\n', '') for item in memInfo]
        memInfo = [item.lower() for item in memInfo]
        mtIndex = [item.find('memtotal') for item in memInfo]
        maIndex = [item.find('memavailable') for item in memInfo]
        if (0 in mtIndex) and (0 in maIndex): 
            memTotal = memInfo[mtIndex.index(0)].split(':')[1].strip()
            memAvail = memInfo[maIndex.index(0)].split(':')[1].strip()
            memTtl = int(memTotal.split()[0])
            memAvlbl = int(memAvail.split()[0])
            memUsd = int(memTtl - memAvlbl)
            unit = memTotal.split()[1].strip().lower()
            ramPercent = int((memUsd / memTtl) * 100)
            if (memTtl > 1024**5):
                coefficient = 1024**5
            elif (memTtl > 1024**4):
                coefficient = 1024**4
            elif (memTtl > 1024**3):
                coefficient = 1024**3
            elif (memTtl > 1024**2):
                coefficient = 1024**2
            elif (memTtl > 1024**1):
                coefficient = 1024**1
            else:
                coefficient = 1
            memTtl /= coefficient
            memUsd /= coefficient
            if (unit == 'b'):
                if (coefficient == 1024**5): unit = 'PB'
                elif (coefficient == 1024**4): unit = 'TB'
                elif (coefficient == 1024**3): unit = 'GB'
                elif (coefficient == 1024**2): unit = 'MB'
                elif (coefficient == 1024**1): unit = 'KB'
                elif (coefficient == 1): unit = 'B'
            elif (unit == 'kb'):
                if (coefficient == 1024**4): unit = 'PB'
                elif (coefficient == 1024**3): unit = 'TB'
                elif (coefficient == 1024**2): unit = 'GB'
                elif (coefficient == 1024**1): unit = 'MB'
                elif (coefficient == 1): unit = 'KB'
            elif (unit == 'mb'):
                if (coefficient == 1024**3): unit = 'PB'
                elif (coefficient == 1024**2): unit = 'TB'
                elif (coefficient == 1024**1): unit = 'GB'
                elif (coefficient == 1): unit = 'MB'
            elif (unit == 'gb'):
                if (coefficient == 1024**2): unit = 'PB'
                elif (coefficient == 1024**1): unit = 'TB'
                elif (coefficient == 1): unit = 'GB'
            elif (unit == 'tb'):
                if (coefficient == 1024**1): unit = 'PB'
                elif (coefficient == 1): unit = 'TB'
            elif (unit == 'pb'):
                if (coefficient == 1): unit = 'PB'
        else:
            ramPercent = -1
        ramUsage.append('amt_used:' + '{0:.1f}'.format(memUsd) + ' ' + unit)
        ramUsage.append('amt_total:' + '{0:.1f}'.format(memTtl) + ' ' + unit)
    except Exception as ex:
        ramPercent = -1
        ramUsage = []
        ramUsage.append('amt_used:' + '{0:.1f}'.format(-1) + ' ' + 'B')
        ramUsage.append('amt_total:' + '{0:.1f}'.format(-1) + ' ' + 'B')
    finally:
        return ramPercent, ramUsage

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as file:
            uptimeSeconds = float(file.readline().split()[0])
        uptimeCalc = str(datetime.timedelta(seconds=uptimeSeconds))
        uptimeDays = uptimeCalc.split(',')[0].strip()
        uptimeHMS = uptimeCalc.split(',')[1].strip()
        upTime = uptimeDays + ', ' + uptimeHMS.split(':')[0] + ' hours, ' + uptimeHMS.split(':')[1] + ' minutes'
    except Exception as ex:
        upTime = '-1 days, -1 hours, -1 minutes'
    finally:
        return upTime