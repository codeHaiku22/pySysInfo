import datetime
import platform

def get_architecture_list():
    try:
        architecture = []
        architecture.append('bit:' + str(platform.architecture()[0]).strip())
        architecture.append('executable:' + str(platform.architecture()[1]).strip())
        architecture.append('machine:' + str(platform.machine()).strip())
        architecture.append('processor:' + str(platform.processor()).strip())
    except Exception as ex:
        architecture = []
        architecture.append('bit:unknown')
        architecture.append('executable:unknown')
        architecture.append('machine:unknown')
        architecture.append('processor:unknown')
    finally:
        return architecture

def get_current_datetime():
    try:
        current_datetime = datetime.datetime.now().strftime('%A, %B %d, %Y  %r')
        #current_datetime = datetime.datetime.now().strftime('%A, %B %d, %Y  %X')
    except Exception as ex:
        current_datetime = 'Monday, January 1, 1900  12:00:01 AM'
    finally:
        return current_datetime

def get_kernel_info_list():
    try:
        kernelInfo = []
        kernel = platform.uname().release.strip()
        isMicrosoftWSL = 'True' if ('wsl' in kernel.lower() or 'microsoft' in kernel.lower()) else 'False'
        kernelInfo.append('kernel:' + kernel)
        kernelInfo.append('microsoftWSL:' + isMicrosoftWSL)
    except Exception as ex:
        kernelInfo = []
        kernelInfo.append('kernel:unknown')
        kernelInfo.append('microsoftWSL:False')
    finally:
        return kernelInfo