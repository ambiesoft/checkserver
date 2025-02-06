#
# To install libralies...
# >pip install

# create 'config.py' from 'config.py.sample'
import config

import os
import tkinter as tk
from tkinter import messagebox
import urllib.request
import urllib.error
import datetime
import re
from datetime import datetime

# pip install dnspython
import dns.resolver

import inspect
import certifi

from lsPy import logger

APPNAME = 'checkserver'

root = tk.Tk()
# root.withdraw() # Do not let a small window to show

logging = None
MYDOMAIN = 'ambiesoft.com'
MYSEARVER_LOCALIP = '192.168.3.97'
MYBLOGURL = "https://ambiesoft.com/blog/"
MYMINERVAURL = "https://ambiesoft.com/minerva/archives/2066"
MYPYONURL = "https://ambiesoft.com/maruchi/pyon/archives/127"

CHECKBLOGLIST = [
    {
        'name': 'blog',
        'findstring': 'ブーログ',
        'url': MYBLOGURL,
    },
    {
        'name': 'minerva',
        'findstring': '偉大ブログ',
        'url': MYMINERVAURL,
    },
    {
        'name': 'pyon',
        'findstring': 'ぴょんぴょんブログ',
        'url': MYPYONURL,
    },
]


def openUrl(url):
    return urllib.request.urlopen(url, cafile=certifi.where())


def checkdns():
    logging.write(inspect.currentframe().f_code.co_name)
    import socket
    addr1 = socket.gethostbyname(MYDOMAIN)
    if addr1 != MYSEARVER_LOCALIP:
        raise (NameError('not ' + MYSEARVER_LOCALIP))
    logging.write("{} is {}".format(MYDOMAIN, addr1))


def checkblogs():
    for blogitem in CHECKBLOGLIST:
        logging.write("{} for {}".format(
            inspect.currentframe().f_code.co_name, blogitem["name"]))
        fp = openUrl(blogitem['url'])
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()

        if -1 == mystr.find(blogitem['findstring']):
            raise (IOError('not blog'))
        if -1 == mystr.find('4755653727306095'):
            raise (IOError('No Adsense in {}. Add {} on the header.php'.format(
                blogitem['name'], '<script data-ad-client="ca-pub-4755653727306095" async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>')))


DBCHECKURL = "https://ambiesoft.com/boolog/dbcheck"


def checkdb():
    logging.write(inspect.currentframe().f_code.co_name)
    fp = openUrl(DBCHECKURL)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()

    if -1 == mystr.find('dbcheck is ok'):
        raise (IOError('db is not ok'))
    logging.write("{} is OK".format(DBCHECKURL))


def check_from_remote():
    ''' open google translate of https://ambiesoft.com/remotecheck.txt and check whether
    specified string is found '''

    logging.write(inspect.currentframe().f_code.co_name)

    SITE_HTML_STRING = '32F79CE2-E088-497B-A6C9-9E906D54AE5F'

    fp = openUrl(
        'https://ambiesoft-com.translate.goog/remotecheck.txt?_x_tr_sl=en&_x_tr_tl=ja&_x_tr_hl=ja&_x_tr_pto=wapp')
    mybytes = fp.read()
    mystr = mybytes.decode('utf8')

    if -1 == mystr.find(SITE_HTML_STRING):
        raise (IOError('My site can not be accessed from outside.'))


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
    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', allhtml)[0]
    if not ip:
        raise (IOError('current ip not found'))
    return ip


def getip():
    logging.write(inspect.currentframe().f_code.co_name)
    fp = urllib.request.urlopen("http://checkip.dyndns.com/")
    ipstr = fp.read().decode("utf8")
    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ipstr)[0]
    if not ip:
        raise (IOError('current ip not found'))
    return ip


def checkip():
    logging.write(inspect.currentframe().f_code.co_name)

    ip = getip2()
    logging.write("Current IP is {}".format(ip))

    my_resolver = dns.resolver.Resolver()

    # 8.8.8.8 is Google's public DNS server
    my_resolver.nameservers = ['8.8.8.8']
    answers = my_resolver.resolve(MYDOMAIN, 'A')
    for answer in answers:
        dnsip = answer.to_text()
        break

    logging.write("DNS(8.8.8.8) IP is {}".format(dnsip))

    if ip != dnsip:
        raise (NameError('Current ip != dns ip ({} != {}'.format(ip, dnsip)))


def modifyAsSpecialLogLine(line):
    ''' Add ---------- on the line '''
    return f'---------- {line} ----------'


def errorEnd(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messagebox.showerror(APPNAME, f"{current_time}\n\n{message}")


def main():
    global logging
    logging = logger.Logger()
    logging.write(modifyAsSpecialLogLine('started'))

    checkdns()
    checkblogs()
    checkdb()
    checkip()
    check_from_remote()

    logging.write(modifyAsSpecialLogLine('ended'))
    del logging


if __name__ == '__main__':
    try:
        main()
    except urllib.error.HTTPError as e:
        errorEnd('{}, URL={}'.format(repr(e), e.filename))
    except Exception as e:
        errorEnd(repr(e) + type(e).__name__)
