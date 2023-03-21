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

1. Start multiple instances of the `node` class with different ports.

2. Use the provided API endpoints to interact with the blockchain network, such as adding new bindings or querying existing bindings.

3. Monitor the network through the `getData()` method to check the current leader, the height of the blockchain, and the list of nodes.

## API Endpoints

- `/vote_request`: Initiates a synchronizer election.
- `/receive_heartbeat`: Receives a heartbeat message from the synchronizer.
- `/get_chain`: Retrieves the current blockchain from the synchronizer.
- `/receive_block`: Receives a new block from another node.

## License

[MIT](https://choosealicense.com/licenses/mit/)