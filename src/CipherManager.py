# -*- coding: utf-8 -*-

class CipherManager:
    
    ZKARRAY = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
        'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
        'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
        'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y', 'Z', '0', '1', '2', '3',
        '4', '5', '6', '7', '8', '8', '-', '_'
    ]

    HASH_ZKARRAY = {
        'a': 0,  'b': 1,  'c': 2,  'd': 3,  'e': 4,  'f': 5,  'g': 6,  'h': 7,
        'i': 8,  'j': 9,  'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15,
        'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23,
        'y': 24, 'z': 25, 'A': 26, 'B': 27, 'C': 28, 'D': 29, 'E': 30, 'F': 31,
        'G': 32, 'H': 33, 'I': 34, 'J': 35, 'K': 36, 'L': 37, 'M': 38, 'N': 39,
        'O': 40, 'P': 41, 'Q': 42, 'R': 43, 'S': 44, 'T': 45, 'U': 46, 'V': 47,
        'W': 48, 'X': 49, 'Y': 50, 'Z': 51, '0': 52, '1': 53, '2': 54, '3': 55,
        '4': 56, '5': 57, '6': 58, '7': 59, '8': 60, '8': 61, '-': 62, '_': 63
    }

    def encryptIp(decryptedIp):
        values = decryptedIp.split('.')
        i = 0
        encryptedIp = ""
        while i < 4:
            a = int(values[i])
            x = (a >> 4) & 15
            y = a & 15
            b = chr(x + 48)
            c = chr(y + 48)
            encryptedIp += b + c
            i += 1
        return (encryptedIp)

    def decryptIp(encryptedIp):
        i = 0
        decryptedIp = ""
        while i < 8:
            a = ord(encryptedIp[i]) - 48
            b = ord(encryptedIp[i + 1]) - 48
            c = ((a & 15) << 4) | (b & 15)
            if i != 0:
                decryptedIp += '.'
            decryptedIp += str(c)
            i += 2
        return (decryptedIp)
    
    def encryptPort(decryptedPort):
        a = (decryptedPort >> 12) & 63
        b = (decryptedPort >> 6) & 63
        c = decryptedPort & 63
        encryptedPort = CipherManager.ZKARRAY[a] + CipherManager.ZKARRAY[b] + CipherManager.ZKARRAY[c]
        return (encryptedPort)
    
    def decryptPort(encryptedPort):
        a = CipherManager.HASH_ZKARRAY[encryptedPort[0]] & 63
        b = CipherManager.HASH_ZKARRAY[encryptedPort[1]] & 63
        c = CipherManager.HASH_ZKARRAY[encryptedPort[2]] & 63
        decryptedPort = (a << 12) | (b << 6) | c
        return (decryptedPort)