import tkinter as tk 
from tkinter import messagebox 
import urllib.request

APPNAME = 'checkserver'

root = tk.Tk() 
root.withdraw() #小さなウィンドウを表示させない 

def checkdns():
    import socket
    addr1 = socket.gethostbyname('ambiesoft.mooo.com') 
    if addr1 != '192.168.3.99':
        raise(NameError('not 192.168.3.99'))

def checkblog():
    fp = urllib.request.urlopen("http://ambiesoft.mooo.com/blog/")
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    if -1 == mystr.find('ﾌﾞｰログ'):
        raise(IOError('not blog'))

def checkdb():
    fp = urllib.request.urlopen("http://ambiesoft.mooo.com/boolog/dbcheck")
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    if -1 == mystr.find('dbcheck is ok'):
        raise(IOError('db is not ok'))

    
def main():
    try:
        checkdns()
        # messagebox.showinfo('title', 'message')
        checkblog()
        checkdb()

    except Exception as e:
        messagebox.showerror(APPNAME, repr(e)) #APPNAME, type(e).__name__ + (str)e)


if __name__ == '__main__':
    main()