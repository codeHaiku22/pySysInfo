def get_forecast(location, verbosity):
    try:
        import requests
        complete = requests.get('http://wttr.in/' + location).text.split('\n')
        if (verbosity == 3):
            i = 0
            max = 37
        elif (verbosity == 2):
            i = 0
            max = 17
        elif (verbosity == 1):
            i = 1
            max = 7
        forecast = ''
        while i < max:
            forecast += complete[i] + '\n'
            i+= 1
        if (verbosity != 1): forecast += complete[37] + '\n'
    except Exception as ex:
        forecast = 'unknown'
    finally:
        return forecast

def get_dad_joke():
    try:
        import requests
        dadJoke = requests.get('https://icanhazdadjoke.com').text
    except Exception as ex:
        dadJoke = 'unknown'
    finally:
        return dadJoke

def get_external_ip_address():
    try:
        import requests
        #externalIP = requests.get('http://api.ipify.org').text
        externalIP = requests.get('http://ifconfig.me').text.strip()
    except Exception as ex:
        externalIP = 'unknown'
    finally:
        return externalIP    