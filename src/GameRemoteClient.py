# -*- coding: utf-8 -*-

import socket

from threading import Thread

from src.PacketParser import PacketParser
from src.DatabaseManager import DatabaseManager
from src.Logger import Logger

class GameRemoteClient(Thread):
    
    def __init__(self, localClient, serverIp, serverPort):
        Thread.__init__(self)

        self.localClient = localClient
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverIp = serverIp
        self.serverPort = serverPort
        self.connected = False
        self.parser = PacketParser()

    def send(self, data):
        if self.connected:
            self.socket.sendall(data)
            return True
        return False

    def processPackets(self):
        newPacket = self.parser.getPacket()
        while newPacket:
            Logger.debug("[GAME] << " + newPacket)
            DatabaseManager().addPacket(0, newPacket)
            data = bytearray(newPacket.encode("utf-8"))
            data += b'\x00'
            if self.localClient.send(data) == False:
                self.socket.close()
                Logger.info("[GAME] Server disconnected")
                return (False)
            newPacket = self.parser.getPacket()
        return (True)


    def run(self):
        self.socket.connect((self.serverIp, self.serverPort))
        self.connected = True
        recvData = self.socket.recv(4096)
        while recvData:
            self.parser.feed(recvData)
            if self.processPackets() == False:
                return (False)
            recvData = self.socket.recv(4096)
        self.connected = False
        Logger.info("[GAME] Server disconnected")
