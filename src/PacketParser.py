# -*- coding: utf-8 -*-

class PacketParser:
    
    def __init__(self):
        self.buff = bytearray()

    def feed(self, buff):
        self.buff += bytearray(buff)
    
    def findEnd(self):
        i = 0
        while i < len(self.buff):
            if self.buff[i] == 0x00:
                return (i)
            i += 1
        return (-1)
    
    def getPacket(self):
        size = self.findEnd()
        if size != -1:
            newPacket = self.buff[:size]
            self.buff = self.buff[(size + 1):]
            return (newPacket.decode('utf-8'))
        return (None)
