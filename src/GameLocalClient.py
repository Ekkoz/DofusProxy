# -*- coding: utf-8 -*-

import socket

from threading import Thread

from src.GameRemoteClient import GameRemoteClient
from src.PacketParser import PacketParser
from src.DatabaseManager import DatabaseManager
from src.Logger import Logger

class GameLocalClient(Thread):
    
    def __init__(self, serverIp, serverPort):
        Thread.__init__(self)

        self.listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listeningSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.serverIp = serverIp
        self.serverPort = serverPort

        self.connected = False
        self.parser = PacketParser()

    def getListeningIp(self):
        return (self.listeningSocket.getsockname()[0])

    def getListeningPort(self):
        return (self.listeningSocket.getsockname()[1])
    
    def listen(self):
        try:
            self.listeningSocket.bind(("127.0.0.1", 0))
        except socket.error as msg:
            Logger.error('[GAME] Bind failed. Error : ' + str(sys.exc_info()))
            return (False)
        
        self.listeningSocket.listen(1)

    def send(self, data):
        if self.connected:
            self.fd.sendall(data)
            return True
        return False

    def processPackets(self):
        newPacket = self.parser.getPacket()
        while newPacket:
            Logger.debug("[GAME] >> " + newPacket)
            DatabaseManager().addPacket(1, newPacket)
            data = bytearray(newPacket.encode("utf-8"))
            data += b'\x00'
            if self.remoteServer.send(data) == False:
                self.fd.close()
                Logger.info("[GAME] Client " + self.ip + ":" + self.port + " disconnected")
                return (False)
            newPacket = self.parser.getPacket()
        return (True)

    def run(self):
        Logger.info("[GAME] Listening on " + self.getListeningIp() + ":" + str(self.getListeningPort()) + "...")

        self.fd, self.addr = self.listeningSocket.accept()
        self.ip, self.port = str(self.addr[0]), str(self.addr[1])
        Logger.info('[GAME] New incomming connection: ' + self.ip + ':' + self.port)

        self.listeningSocket.close()

        self.connected = True
        self.remoteServer = GameRemoteClient(self, self.serverIp, self.serverPort)
        self.remoteServer.start()
        recvData = self.fd.recv(4096)
        while recvData:
            self.parser.feed(recvData)
            if self.processPackets() == False:
                return (False)
            recvData = self.fd.recv(4096)
        self.connected = False
        Logger.info("[GAME] Client " + self.ip + ":" + self.port + " disconnected")
