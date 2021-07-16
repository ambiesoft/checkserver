#
# To install libralies...
# >pip install

import os
import tkinter as tk 
from tkinter import messagebox 
import urllib.request
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

def checkip():
    logging.write(inspect.currentframe().f_code.co_name)
    fp = urllib.request.urlopen("http://checkip.dyndns.com/")
    ipstr = fp.read().decode("utf8")
    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', ipstr )[0]
    if not ip:
        raise(IOError('current ip not found'))
    
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
    except Exception as e:
        messagebox.showerror(APPNAME, repr(e)) #APPNAME, type(e).__name__ + (str)e)
