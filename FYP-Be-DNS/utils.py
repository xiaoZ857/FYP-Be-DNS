from hashlib import sha256
from datetime import datetime


def getTime():
    now = datetime.now()
    time = now.strftime("%Y-%m-%d, %H:%M:%S")
    return time

def getHash(data):
    return sha256(data.encode()).hexdigest()



