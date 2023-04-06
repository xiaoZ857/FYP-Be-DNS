# Import required libraries
from dataclasses import dataclass
from hashlib import sha256
from datetime import datetime
import random
import threading
import time
import requests
import json

# Define the list of nodes
NODES = ['127.0.0.1:5000','127.0.0.1:5001','127.0.0.1:5002','127.0.0.1:5003','127.0.0.1:5004']

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
        # debug 20230321
        print(self.NametoIpmap, type(self.NametoIpmap))
        if (self.checkVaild == False):
            return 'invaild blockchain log'
        if self.NametoIpmap.get(getHash(domainName), 'not exist') == 'not exist':
            return 'Corresponding IP address does not exist'
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
        self.nodes = NODES
        self.blockchain = blockchain
        self.leader = None
        self.state = 'candidate'
        self.url = url
        self.voted = False
        self.votes_received = 0
        self.received = True
        self.majority = ((len(self.nodes) - 1) // 2)
        self.timeout = random.uniform(1, 5)
        self.timer = threading.Timer(self.timeout, self.runtime)
        self.timer.start()

    def runtime(self):
        time.sleep(5)
        while True:
            if self.state == 'candidate':
                self.start_election()
            elif self.state == 'leader':
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
            if node == self.url:
                continue
            response = requests.post(f'http://{node}/vote_request', json=election)
            if response.status_code == 200:
                if response.json()['vote'] == 'yes':
                    self.votes_received += 1

        if self.votes_received >= self.majority:
            self.leader = self.url
            self.state = 'leader'
        else:
            self.state = 'follower'
            
    def send_heartbeat(self):
        while self.state == 'leader':
            heart_received = 0
            time.sleep(5+random.uniform(1, 2))
            leader = {
                'height': len(self.blockchain.chain),
                'hash': self.blockchain.getMapHash,
                'term': self.term,
                'url':self.url
            }
            for node in self.nodes:
                if node == self.url:
                    continue
                response = requests.post(f'http://{node}/receive_heartbeat', data=leader)
                if response.status_code == 200:
                    heart_received += 1

            if heart_received < self.majority:
                self.state = 'candidate'

    def recover(self):
        response = requests.get(f'http://{self.leader}/get_chain')
        if response.status_code == 200:
            self.blockchain.chain = response['chain']
            self.blockchain.NametoIpmap = response['NametoIpmap']
            self.blockchain.NametoOwnermap = response['NametoOwnermap']

    def follower(self):
        self.voted = False
        while True:
            self.received == False
            time.sleep(10+random.uniform(1, 2))
            if self.received == False:
                self.state = 'candidate'

    def broadcast_block(self):
        newblock = self.blockchain.chain[-1]
        newNametoIpmap = self.blockchain.NametoIpmap
        newNametoOwnermap = self.blockchain.NametoOwnermap
        data = {
            'url':self.url,
            'index':newblock.index,
            'previousHash':newblock.previousHash,
            'timestamp':newblock.timestamp,
            'mapHash':newblock.mapHash,
            'hash':newblock.hash,
            'newNametoIpmap': json.dumps(newNametoIpmap),
            'newNametoOwnermap': json.dumps(newNametoOwnermap),
        }
        print ('broadcasting block')
        for node in self.nodes:
            if node == self.url:
                continue
            response = requests.post(f'http://{node}/receive_block', data=data)

    def getData(self):
        if self.leader != None:
            data = {
                'leader': self.leader,
                'height':len(self.blockchain.chain),
                'nodes':self.nodes,
            }
        else:
            data = {
                'leader': 'in election',
                'height':len(self.blockchain.chain),
                'nodes':self.nodes,
            }
        return data
