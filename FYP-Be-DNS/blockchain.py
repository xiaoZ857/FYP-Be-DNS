from dataclasses import dataclass
from hashlib import sha256
from datetime import datetime
from flask import Flask, request
import requests
import rsa
import json

def getTime():
    now = datetime.now()
    time = now.strftime("%Y-%m-%d, %H:%M:%S")
    return time

def getHash(data):
    return sha256(data.encode()).hexdigest()

class blockchain:   
    def __init__(self):    
        self.chain = []
        self.NametoIpmap = {}
        self.NametoOwnermap = {}
        genesisBlock = block(0, 0x0, getTime(), 0x0)
        self.chain.append(genesisBlock)

    def getPreviousHash(self):
        return self.chain[-1].hash

    def getMapHash(self):
        mapHash = getHash(str(self.NametoIpmap))
        return mapHash

    def checkVaild(self):
        check = (self.chain[-1].mapHash == self.getMapHash())&(self.chain[-1].previousHash == self.chain[-2].hash)
        return check

    def addNewBlock(self):
        newBlock = block(len(self.chain), self.getPreviousHash(), getTime(), self.getMapHash())
        self.chain.append(newBlock)

    def addNewBinding(self, domainName, ip, owner):
        assert self.NametoIpmap.get(getHash(domainName), 'not exist') == 'not exist', 'Domain Name used'
        self.NametoIpmap[getHash(domainName)] = str(ip)
        self.NametoOwnermap[getHash(domainName)] = getHash(owner)
        self.addNewBlock()

    def changeBinding(self, domainName, Newip, owner):
        assert self.NametoOwnermap.get(getHash(domainName), 'not exist') != 'not exist', 'Domain Name not exist'
        assert self.NametoOwnermap.get(getHash(domainName), 'not exist') == getHash(owner), 'Invaild user'
        self.NametoIpmap[getHash(domainName)] = str(Newip)
        self.addNewBlock()

    def queryBinding(self, domainName):
        assert self.checkVaild, 'Invaild blockchain log'
        assert self.NametoIpmap.get(getHash(domainName), 'not exist') != 'not exist', 'Corresponding IP address not exist'
        return self.NametoIpmap[getHash(domainName)]

    def showBlock(self, index):
        selected_block = self.chain[index]
        print('{')
        print('index: ' + str(selected_block.index))
        print('previousHash: ' + str(selected_block.previousHash))
        print('timestamp: ' + str(selected_block.timestamp))
        print('mapHash: ' + str(selected_block.mapHash))
        print('} => Hash: ' + str(selected_block.hash))
        print('-'*80)

    def showAllBlock(self):
        for i in range(len(self.chain)):
            self.showBlock(i)

class block:
    def __init__(self, index, previousHash, timestamp, mapHash):    
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.mapHash = mapHash
        self.blockjson = {
                            'index': self.index,
                            'previousHash': self.previousHash,
                            'timestamp': self.timestamp,
                            'mapHash': self.mapHash,
                        }
        self.hash = sha256(json.dumps(self.blockjson).encode()).hexdigest()

class account:
    def __init__(self):
        (publickey, privatekey) = rsa.newkeys(512)
        self.privateKey = privatekey
        self.publicKey = publickey

    def encrypt(self, text):
        cipher = rsa.encrypt(bytes(text, encoding='utf-8'), self.publicKey)
        return cipher

    def decrypt(self, encrypt_text):
        plain = rsa.decrypt(encrypt_text, self.privateKey)
        return str(plain, encoding = "utf-8")

    def sign(self, hash):
        signature = rsa.sign(bytes(hash, encoding='utf-8'), self.privateKey, 'SHA-256')
        return signature

    def verify(self, signature, hash):
        method = rsa.verify(bytes(hash, encoding='utf-8'), signature, self.publicKey)
        return method == 'SHA-256'