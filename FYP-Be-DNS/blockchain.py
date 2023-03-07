from dataclasses import dataclass
from hashlib import sha256
from datetime import datetime
import json
import random

def getTime():
    now = datetime.now()
    time = now.strftime("%Y-%m-%d, %H:%M:%S")
    return time

def getHash(data):
    return sha256(data.encode()).hexdigest()

def verify(key, ran, publickey):
    pk = getHash(str(ran) + str(key))
    if(pk == str(publickey)):
        return True
    else:
        return False

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
        mapHash = getHash(str(self.NametoIpmap) + str(self.NametoOwnermap))
        return mapHash

    def checkVaild(self):
        check = (self.chain[-1].mapHash == self.getMapHash())&(self.chain[-1].previousHash == self.chain[-2].hash)
        return check

    def addNewBlock(self):
        newBlock = block(len(self.chain), self.getPreviousHash(), getTime(), self.getMapHash())
        self.chain.append(newBlock)

    def addNewBinding(self, domainName, ip, owner, key, ran):
        if (verify(key, ran, owner)):
            if (self.NametoIpmap.get(getHash(domainName), 'not exist') != 'not exist'):
                return 'Domain Name used'
            self.NametoIpmap[getHash(domainName)] = str(ip)
            self.NametoOwnermap[getHash(domainName)] = getHash(owner)
            self.addNewBlock()
            return 'Successfully added'
        else:
            return 'incorrect key or account'

    def changeBinding(self, domainName, Newip, owner, key, ran):
        if (verify(key, ran, owner)):
            if (self.NametoOwnermap.get(getHash(domainName), 'not exist') == 'not exist'):
                return 'Domain Name not exist'
            if (self.NametoOwnermap.get(getHash(domainName), 'not exist') != getHash(owner)):
                return 'invaild user'
            self.NametoIpmap[getHash(domainName)] = str(Newip)
            self.addNewBlock()
            return 'Successfully changed'
        else:
            return 'incorrect key or account'
        

    def queryBinding(self, domainName):
        if (self.checkVaild == False):
            return 'invaild blockchain log'
        if (self.NametoIpmap.get(getHash(domainName), 'not exist') == 'not exist'):
            return 'Corresponding IP address not exist'
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
    def __init__(self, key):
        ran = random.randint(1,1000000000)
        publickey = getHash(str(ran) + str(key))
        self.key = key
        self.ran = ran
        self.publickey = publickey

    def getKey(self):
        return self.key, self.ran, self.publickey