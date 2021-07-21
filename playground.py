import tkinter as tk 
from tkinter import messagebox 
import urllib.request
import urllib.error

APPNAME = 'PLAYGROUND'
MYBLOGURL = "https://ambiesoft.com/blog/aaaaaaaaaaaaaaaaaaaaaa"

def main():
    fp = urllib.request.urlopen(MYBLOGURL)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()

    if -1 == mystr.find('ﾌﾞｰログ'):
        raise(IOError('not blog'))

if __name__ == '__main__':
    try:    
        main()
    except urllib.error.HTTPError as e:
        messagebox.showerror(APPNAME, 
            '{}, URL={}'.format(repr(e), e.filename))
    except Exception as e:
        messagebox.showerror(APPNAME, 
            'ExceptionName={}, REPR={}'.format(type(e).__name__, repr(e)))

