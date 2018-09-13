# -*- coding: utf-8 -*-

import socket

from threading import Thread

from src.GameLocalClient import GameLocalClient

from src.PacketParser import PacketParser
from src.CipherManager import CipherManager
from src.DatabaseManager import DatabaseManager

class RealmRemoteClient(Thread):
    
    def __init__(self, localClient):
        Thread.__init__(self)

        self.localClient = localClient
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.parser = PacketParser()

    def send(self, data):
        if self.connected:
            self.socket.sendall(data)
            return True
        return False

    def parsePacket(self, packet):
        if len(packet) > 3 and packet[0] == 'A' and packet[1] == 'X' and packet[2] == 'K':
            print("[+] [REALM] onSelectServer packet detected!")
            encryptedIp = packet[3:11]
            encryptedPort = packet[11:14]
            ticket = packet[14:]
            decryptedIp = CipherManager.decryptIp(encryptedIp)
            decryptedPort = CipherManager.decryptPort(encryptedPort)
            newGameClient = GameLocalClient(decryptedIp, decryptedPort)
            newGameClient.listen()
            newEncryptedIp = CipherManager.encryptIp(newGameClient.getListeningIp())
            newEncryptedPort = CipherManager.encryptPort(newGameClient.getListeningPort())
            newPacket = "AXK" + newEncryptedIp + newEncryptedPort + ticket
            print("[+] [REALM] Replacing packet '" + packet + "' with packet '" + newPacket + "'")
            newGameClient.start()
            return (newPacket)
        return (packet)


    def processPackets(self):
        newPacket = self.parser.getPacket()
        while newPacket:
            print("[+] [REALM] << " + newPacket)
            DatabaseManager().addPacket(0, newPacket)
            newPacket = self.parsePacket(newPacket)
            data = bytearray(newPacket.encode("utf-8"))
            data += b'\x00'
            if self.localClient.send(data) == False:
                self.socket.close()
                print("[+] [REALM] Server disconnected")
                return (False)
            newPacket = self.parser.getPacket()
        return (True)


    def run(self):
        self.socket.connect(("34.251.172.139", 443))
        self.connected = True
        recvData = self.socket.recv(4096)
        while recvData:
            self.parser.feed(recvData)
            if self.processPackets() == False:
                return (False)
            recvData = self.socket.recv(4096)
        self.connected = False
        print("[+] [REALM] Server disconnected")
