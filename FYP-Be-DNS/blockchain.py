from dataclasses import dataclass
from hashlib import sha256
from datetime import datetime
import json
import random
import threading
import time
import requests

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
        genesisBlock = block(0, 0x0, "hello world", 0x0)
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
        self.hash = getHash(str(index)+str(previousHash)+str(timestamp)+str(mapHash))

class account:
    def __init__(self, key):
        ran = random.randint(1,1000000000)
        publickey = getHash(str(ran) + str(key))
        self.key = key
        self.ran = ran
        self.publickey = publickey

    def getKey(self):
        return self.key, self.ran, self.publickey


class node:
    def __init__(self, blockchain, url):
        self.term = 0
        self.nodes = set()
        self.blockchain = blockchain
        self.syncer = None
        self.state = 'candidate'
        self.url = url
        self.voted = False
        self.votes_received = 0
        self.received = True
        self.majority = ((len(self.nodes) - 1) // 2)
        self.syncer_timeout = random.uniform(1, 5)
        self.timer = threading.Timer(self.syncer_timeout, self.runtime)
        self.timer.start()


    def runtime(self):
        while True:
            if self.state == 'candidate':
                self.start_election()
            elif self.state == 'syncer':
                self.send_heartbeat()
            elif self.state == 'follower':
                self.follower()
            time.sleep(1)


    def start_election(self):
        self.term += 1
        election = {
            'term':self.term,
            'url':self.url,
        }
        for node in self.nodes:
            response = requests.post(f'http://{node}/vote_request', json=election)
            if response.status_code == 200:
                if response.json()['vote'] == 'yes':
                    self.votes_received += 1

        if self.votes_received >= self.majority:
            self.syncer = self.url
            self.state = 'syncer'
        else:
            self.state = 'follower'
            

    def send_heartbeat(self):
        while self.state == 'syncer':
            heart_received = 0
            time.sleep(5+random.uniform(1, 2))
            syncer = {
                'height': len(self.blockchain.chain),
                'hash': self.blockchain.getMapHash,
                'term': self.term,
                'url':self.url
            }
            for node in self.nodes:
                response = requests.post(f'http://{node}/receive_heartbeat', json=syncer)
                if response.status_code == 200:
                    heart_received += 1

            if heart_received < self.majority:
                self.state = 'candidate'


    def recover(self):
        response = requests.get(f'http://{self.syncer}/get_chain')
        if response.status_code == 200:
            self.blockchain.chain = response.json()['chain']
            self.blockchain.NametoIpmap = response.json()['NametoIpmap']
            self.blockchain.NametoOwnermap = response.json()['NametoOwnermap']

    def follower(self):
        self.voted = False
        while True:
            self.received is False
            time.sleep(10+random.uniform(1, 2))
            if self.received is False:
                self.state = 'candidate'

    def broadcast_block(self):
        newblock = self.blockchain.chain[-1]
        newNametoIpmap = self.blockchain.NametoIpmap
        newNametoOwnermap = self.blockchain.NametoOwnermap
        data = {
            'index':newblock.index,
            'previousHash':newblock.previousHash,
            'timestamp':newblock.timestamp,
            'mapHash':newblock.mapHash,
            'hash':newblock.hash,
            'newNametoIpmap':newNametoIpmap,
            'newNametoOwnermap':newNametoOwnermap,
        }
        for node in self.nodes:
            response = requests.post(f'http://{node}/receive_block', json=data)
