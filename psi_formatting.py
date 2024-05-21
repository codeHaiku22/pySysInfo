#!/usr/bin/python

class bcolors:
    BGBLACK = '\033[40m'
    BGRED = '\033[41m'
    BGGREEN = '\033[42m'
    BGBROWN = '\033[43m'
    BGBLUE = '\033[44m'
    BGPURPLE = '\033[45m'
    BGCYAN = '\033[46m'
    BGLIGHTGRAY = '\033[47m'                        
    GRAY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    LIGHTGRAY = '\033[97m'
    NONE = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    STRIKE = '\033[9m'
    UNDERLINE2 = '\033[21m'

def get_usage_sparkline(percent):
    try:
        sparkline = ''
        length = 40
        usage = '#'
        free = '-'
        if (percent < 0):
            free *= (length - 2)
            free = bcolors.GRAY + free + bcolors.NONE
            sparkline = '[' + '<!' + free + ']' + str(percent).rjust(4, ' ') + '%'  
        elif (percent > 100):
            usage *= (length - 2)
            usage = bcolors.RED + usage + bcolors.NONE
            sparkline = '[' + usage + '!>' + ']' + str(percent).rjust(4, ' ') + '%'
        else:
            usage *= (round(length*(percent/100)))
            free *=  (length - len(usage))
            free = bcolors.GRAY + free + bcolors.NONE
            if (percent == 0): 
                usage = bcolors.GRAY + usage + bcolors.NONE
                pctUsed = bcolors.GRAY + str(percent).rjust(4, ' ') + '%'  + bcolors.NONE            
            elif (percent < 80): 
                usage = bcolors.GREEN + usage + bcolors.NONE
                pctUsed = bcolors.GREEN + str(percent).rjust(4, ' ') + '%'  + bcolors.NONE
            elif (percent < 95): 
                usage = bcolors.YELLOW + usage + bcolors.NONE
                pctUsed = bcolors.YELLOW + str(percent).rjust(4, ' ') + '%'  + bcolors.NONE
            elif (percent <= 100): 
                usage = bcolors.RED + usage + bcolors.NONE
                pctUsed = bcolors.RED + str(percent).rjust(4, ' ') + '%'  + bcolors.NONE
            sparkline = '[' + usage + free + ']' + pctUsed
    except Exception as ex:
        message = 'ERROR!'
        preamble = free * int(((length - len(message)) / 2)) 
        postamble = free * (length - len(message) - len(preamble))           
        sparkline = '[' + preamble + message + postamble + ']' + str(percent).rjust(4, ' ') + '%'
    finally:
        return sparkline

def print_help():
    try:
        print('')
        print('PySystemInfo is a utility that provides system statistics, resource usage details, and a customizable weather forecast (optional).')
        print('')
        print('Usage:')
        print('  psi_main [flags]')
        print('')
        print('Flags:')
        print('  -h, --help                  Help for PySystemInfo')
        print('  -w, --weather postalcode n  Display weather forecast in output.  Provide a postalcode and indicate level of detail from 1-3, with 3 being most detailed.')
        print('')
    except Exception as ex:
        print(ex)

def print_output(type, output='', keyLen=0, key='', value='', usagePct=0, usageAmt='', usageTtl='', fsLen=0, fs='', mount=''):
    try:
        if (type.lower() == 'heading'):
            output = '<~~ ' + output + ' ~~>'
            print(bcolors.MAGENTA + output + bcolors.NONE)    
        if (type.lower() == 'simple'):
            print(bcolors.GREEN + output + bcolors.NONE)
        if (type.lower() == 'keyvalue'):
            print(bcolors.CYAN + key.ljust(keyLen) + ':' + bcolors.NONE, value)
        if (type.lower() == 'keyusage'):
            line = bcolors.LIGHTGRAY + key.ljust(keyLen) + ':' + bcolors.NONE + ' ' + get_usage_sparkline(usagePct)
            if (len(usageAmt) > 0): line += bcolors.LIGHTGRAY + ' ' + usageAmt.rjust(10) + ' / ' + usageTtl.ljust(10)
            if (len(fs) > 0): line += bcolors.BLUE + ' ' + fs.ljust(fsLen + 1) + bcolors.NONE + ' ' + bcolors.GRAY + mount
            print(line + bcolors.NONE)
    except Exception as ex:
        print(ex)