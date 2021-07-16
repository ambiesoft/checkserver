#
# To install libralies...
# >pip install playsound

import os
import tkinter as tk 
from tkinter import messagebox 
import urllib.request
import datetime
import re
import dns.resolver

APPNAME = 'checkserver'

root = tk.Tk() 
# root.withdraw() #小さなウィンドウを表示させない 

def checkdns():
    import socket
    addr1 = socket.gethostbyname('ambiesoft.com') 
    if addr1 != '192.168.3.97':
        raise(NameError('not 192.168.3.97'))

def checkblog():
    fp = urllib.request.urlopen("https://ambiesoft.com/blog/")
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()

    if -1 == mystr.find('ﾌﾞｰログ'):
        raise(IOError('not blog'))

def checkdb():
    fp = urllib.request.urlopen("https://ambiesoft.com/boolog/dbcheck")
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()

    if -1 == mystr.find('dbcheck is ok'):
        raise(IOError('db is not ok'))

def checkip():
    fp = urllib.request.urlopen("http://checkip.dyndns.com/")
    ipstr = fp.read().decode("utf8")
    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', ipstr )[0]
    if not ip:
        raise(IOError('current ip not found'))
    
    my_resolver = dns.resolver.Resolver()

    # 8.8.8.8 is Google's public DNS server
    my_resolver.nameservers = ['8.8.8.8']
    # answers = my_resolver.query('ambiesoft.com', 'A')
    answers = my_resolver.resolve('ambiesoft.com', 'A')
    for answer in answers:
        dnsip = answer.to_text()
        break

    if ip != dnsip:
        raise(NameError('Current ip != dns ip ({} != {}'.format(ip,dnsip)))

def playsoundcommon(ok):
    from playsound import playsound
    playsound(os.path.join(os.path.dirname(__file__), 'ok.wav' if ok else 'ng.wav'))
    
def playoksound():
    playsoundcommon(True)

def playngsound():
    playsoundcommon(False)

def main():
    logfilename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.path.splitext(os.path.basename(__file__))[0] + '.log')
    logfile = open(logfilename,'+w')
    logfile.write(str(datetime.datetime.today()))

    try:
        checkdns()
        checkblog()
        checkdb()
        checkip()
        # playoksound()

    except Exception as e:
        messagebox.showerror(APPNAME, repr(e)) #APPNAME, type(e).__name__ + (str)e)
        # playngsound()

    logfile.close()

if __name__ == '__main__':
    messagebox.showerror(APPNAME, 'aaaaaaaaaaaaaaaaaaa')
    main()