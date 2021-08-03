#
# To install libralies...
# >pip install

import os
import tkinter as tk 
from tkinter import messagebox 
import urllib.request
import urllib.error
import datetime
import re
import dns.resolver
import inspect

from lsPy import logger

APPNAME = 'checkserver'

root = tk.Tk() 
# root.withdraw() #小さなウィンドウを表示させない 

logging = None
MYDOMAIN = 'ambiesoft.com'
MYLOCALIP = '192.168.3.97'
MYBLOGURL = "https://ambiesoft.com/blog/"
import config

def checkdns():
    logging.write(inspect.currentframe().f_code.co_name)
    import socket
    addr1 = socket.gethostbyname(MYDOMAIN) 
    if addr1 != MYLOCALIP:
        raise(NameError('not ' + MYLOCALIP))

def checkblog():
    logging.write(inspect.currentframe().f_code.co_name)
    fp = urllib.request.urlopen(MYBLOGURL)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()

    if -1 == mystr.find('ﾌﾞｰログ'):
        raise(IOError('not blog'))

def checkdb():
    logging.write(inspect.currentframe().f_code.co_name)
    fp = urllib.request.urlopen("https://ambiesoft.com/boolog/dbcheck")
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()

    if -1 == mystr.find('dbcheck is ok'):
        raise(IOError('db is not ok'))

def getip2():
    # create a password manager
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

    # Add the username and password.
    # If we knew the realm, we could use it instead of None.
    top_level_url = "http://192.168.3.1/index.cgi/info_main"
    password_mgr.add_password(None, top_level_url, config.USER, config.PASS)

    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

    # create "opener" (OpenerDirector instance)
    opener = urllib.request.build_opener(handler)

    # use the opener to fetch a URL
    opener.open(top_level_url)

    # Install the opener.
    # Now all calls to urllib.request.urlopen use our opener.
    urllib.request.install_opener(opener)

    fp = urllib.request.urlopen(top_level_url)
    allhtml = fp.read().decode("eucjp")
    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', allhtml )[0]
    if not ip:
        raise(IOError('current ip not found'))
    return ip

def getip():
    logging.write(inspect.currentframe().f_code.co_name)
    fp = urllib.request.urlopen("http://checkip.dyndns.com/")
    ipstr = fp.read().decode("utf8")
    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', ipstr )[0]
    if not ip:
        raise(IOError('current ip not found'))
    return ip

def checkip():
    ip = getip2()
    my_resolver = dns.resolver.Resolver()

    # 8.8.8.8 is Google's public DNS server
    my_resolver.nameservers = ['8.8.8.8']
    answers = my_resolver.resolve(MYDOMAIN, 'A')
    for answer in answers:
        dnsip = answer.to_text()
        break

    if ip != dnsip:
        raise(NameError('Current ip != dns ip ({} != {}'.format(ip,dnsip)))

# def playsoundcommon(ok):
#     from playsound import playsound
#     playsound(os.path.join(os.path.dirname(__file__), 'ok.wav' if ok else 'ng.wav'))
    
# def playoksound():
#     playsoundcommon(True)

# def playngsound():
#     playsoundcommon(False)

def main():
    global logging
    logging = logger.Logger()
    logging.write('started')
    checkdns()
    checkblog()
    checkdb()
    checkip()
    logging.write('ended')
    del logging

if __name__ == '__main__':
    try:    
        main()
    except urllib.error.HTTPError as e:
        messagebox.showerror(APPNAME, 
            '{}, URL={}'.format(repr(e), e.filename))        
    except Exception as e:
        messagebox.showerror(APPNAME, repr(e) + type(e).__name__)
