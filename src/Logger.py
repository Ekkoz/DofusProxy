# -*- coding: utf-8 -*-

import datetime
import sys

class Logger:

    def date():
        return (datetime.datetime.now().strftime("%H:%M:%S"))

    def debug(msg):
        print("[*] [" + Logger.date() + "] " + msg)
    
    def info(msg):
        print("[+] [" + Logger.date() + "] " + msg)
    
    def error(msg):
        print("[-] [" + Logger.date() + "] " + msg, file=sys.stderr)
