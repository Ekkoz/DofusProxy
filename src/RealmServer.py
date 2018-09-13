# -*- coding: utf-8 -*-

import socket

from src.RealmLocalClient import RealmLocalClient

class RealmServer:
    
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        try:
            self.socket.bind(("127.0.0.1", 12345))
        except socket.error as msg:
            print('[-] [REALM] Bind failed. Error : ' + str(sys.exc_info()))
            return (False)
        
        self.socket.listen(16)

        print("[+] [REALM] Listening on port 12345...")

        while True:
            fd, addr = self.socket.accept()
            ip, port = str(addr[0]), str(addr[1])
            print('[+] [REALM] New incomming connection: ' + ip + ':' + port)

            newClient = RealmLocalClient(fd, addr, ip, port)
            newClient.start()

        self.socket.close()