# -*- coding: utf-8 -*-

from threading import Thread

from src.RealmRemoteClient import RealmRemoteClient
from src.PacketParser import PacketParser
from src.DatabaseManager import DatabaseManager
from src.Logger import Logger

class RealmLocalClient(Thread):
    
    def __init__(self, fd, addr, ip, port):
        Thread.__init__(self)
        self.fd = fd
        self.addr = addr
        self.ip = ip
        self.port = port
        self.connected = False
        self.parser = PacketParser()

    def send(self, data):
        if self.connected:
            self.fd.sendall(data)
            return True
        return False
    
    def processPackets(self):
        newPacket = self.parser.getPacket()
        while newPacket:
            Logger.debug("[REALM] >> " + newPacket)
            DatabaseManager().addPacket(1, newPacket)
            data = bytearray(newPacket.encode("utf-8"))
            data += b'\x00'
            if self.remoteServer.send(data) == False:
                self.fd.close()
                Logger.info("[REALM] Client " + self.ip + ":" + self.port + " disconnected")
                return (False)
            newPacket = self.parser.getPacket()
        return (True)

    def run(self):
        self.connected = True
        self.remoteServer = RealmRemoteClient(self)
        self.remoteServer.start()
        recvData = self.fd.recv(4096)
        while recvData:
            self.parser.feed(recvData)
            if self.processPackets() == False:
                return (False)
            recvData = self.fd.recv(4096)
        self.connected = False
        Logger.info("[REALM] Client " + self.ip + ":" + self.port + " disconnected")
