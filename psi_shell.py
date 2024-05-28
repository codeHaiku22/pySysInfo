import subprocess

def get_dad_joke():
    try:
        dadJoke = subprocess.run(['curl', '-s', 'https://icanhazdadjoke.com'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True, encoding='utf-8').stdout.strip()
    except Exception as ex:
        dadJoke = 'The funny thing is, there was an error in retrieving a dad joke.'
    finally:
        return dadJoke

def get_external_ip_address():
    try:
        externalIP = subprocess.run(['curl', '-s', 'http://ifconfig.me'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True, encoding='utf-8').stdout.strip()
    except Exception as ex:
        externalIP = 'unknown'
    finally:
        return externalIP
    
def get_forecast(location, detail):
    try:
        complete = subprocess.run(['curl', '-s', 'http://wttr.in'], input=location, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True, encoding='utf-8').stdout.split('\n')
        if (detail == 3):
            i = 0
            max = 37
        elif (detail == 2):
            i = 0
            max = 17
        elif (detail == 1):
            i = 1
            max = 7
        forecast = ''
        while i < max:
            forecast += complete[i] + '\n'
            i+= 1
        if (detail != 1): forecast += complete[37] + '\n'
    except Exception as ex:
        forecast = 'unknown'
    finally:
        return forecast

def get_gpu_list(microsoftWSL):
    try:
        gpu = []
        lspci = subprocess.run(['lspci'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True, encoding='utf-8').stdout.split('\n')
        vga = list(filter(lambda entry: 'Microsoft' in entry, lspci)) if microsoftWSL else list(filter(lambda entry: 'VGA' in entry, lspci))
        for card in vga:
            gpu.append(card.split(':')[-1].strip())
    except Exception as ex:
        gpu = []
        gpu.append('unknown')
    finally:
        return gpu