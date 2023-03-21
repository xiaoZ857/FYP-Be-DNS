# FYP-Be-DNS
A Blockchain-based Domain Name System for Private Network using Raft(SyncRaft)

# SyncRaft Blockchain

This project implements a blockchain network using the SyncRaft consensus algorithm. SyncRaft is a consensus algorithm that maintains the consistency of a blockchain network through a single synchronizer node. This ensures network consistency while allowing each node to add new blocks.

## Features

- Synchronizer node election
- Heartbeat detection for consistency check
- Adding new blocks
- Handling synchronizer failure
- Domain name to IP mapping
- Domain name ownership

## Requirements

- Python 3.x
- Requests library

## Installation

Clone this repository:

```git bash
git clone https://github.com/xiaoZ857/FYP-Be-DNS.git
```

## Usage

1. Start multiple apps with different ports.

2. Use the provided API endpoints to interact with the blockchain network, such as adding new bindings or querying existing bindings.

3. Use the HTML to interact with the network.


## License

[MIT](https://choosealicense.com/licenses/mit/)