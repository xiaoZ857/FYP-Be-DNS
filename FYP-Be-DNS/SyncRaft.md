# SyncRaft Algorithm

SyncRaft is a consensus algorithm that maintains the consistency of a blockchain network through a single synchronizer node. The workflow includes the following steps:

1. **Initialization:**
   - All nodes start with the same state.
   - Each node starts a timer, randomly selects a timeout, and listens for heartbeat messages in the network.
2. **Synchronizer Election:**
   - When a node's timer expires, it initiates a synchronizer election by broadcasting its candidacy to other nodes.
   - Other nodes vote on the candidacy based on certain criteria (e.g., current block height) and return the voting results to the initiating node.
   - If the initiating node receives a majority of votes, it becomes the synchronizer and starts sending periodic heartbeat messages to maintain its status.
3. **Heartbeat Detection:**
   - The synchronizer periodically sends heartbeat messages to other nodes, including its block height and the hash of the stored data.
   - Other nodes perform a self-check upon receiving the heartbeat message and request synchronization from the synchronizer if inconsistencies are found.
4. **Adding New Blocks:**
   - When a node wants to add a new block, it sends a request to the synchronizer.
   - The synchronizer, after confirming all block heights are consistent, informs the node that it can broadcast the new block.
   - The node broadcasts the new block to other nodes. Other nodes validate the new block and add it to their blockchains after validation.
5. **Synchronizer Failure Handling:**
   - If the synchronizer fails or becomes unresponsive, the heartbeat detection timeout of other nodes triggers a new synchronizer election.
   - Once a new synchronizer is elected, the nodes in the network resynchronize their blockchains and resume normal operation.

SyncRaft ensures network consistency through a single synchronizer node while allowing each node to add new blocks. Heartbeat detection and synchronizer election are key mechanisms in this process, ensuring the proper functioning of the synchronizer and maintaining consistency among nodes in the network.

**Advantages**: Each node can add new blocks
**Disadvantages**: Compared to Raft, communication overhead is increased, and since everything ultimately goes through the primary node, it may seem somewhat inefficient.


# SyncRaft算法

SyncRaft是一种共识算法，通过单个同步器节点维护区块链网络的一致性。工作流程包括以下几个步骤：

1. **初始化：**
   - 所有节点以相同的状态开始。
   - 每个节点启动一个计时器，随机选择超时时间，并侦听网络中的心跳消息。
2. **同步器选举：**
   - 当节点的计时器过期时，它通过向其他节点广播自己的候选资格来发起同步器选举。
   - 其他节点根据某些条件（例如，当前区块高度）对候选资格进行投票，并将投票结果返回给发起节点。
   - 如果发起节点获得了大多数投票，它将成为同步器，并开始发送周期性心跳消息以维护其状态。
3. **心跳检测：**
   - 同步器周期性地向其他节点发送心跳消息，其中包括其区块高度，储存数据的哈希。
   - 其他节点在收到心跳消息后做自我检测，如果不一致则向同步器请求同步。
4. **添加新区块：**
   - 当节点想要添加新区块时，它会向同步器发送请求。
   - 同步器在确认所有区块高度一致后，告知节点可以广播。
   - 节点向其他节点广播新区块。其他节点验证新区块，并在验证后将其添加到它们的区块链中。
5. **同步器故障处理：**
   - 如果同步器失败或变得无响应，其他节点的心跳检测超时会触发新的同步器选举。
   - 一旦选出新同步器，网络中的节点将重新同步它们的区块链并恢复正常操作。

SyncRaft通过单个同步器节点确保网络一致性，同时允许每个节点添加新区块。心跳检测和同步器选举是此过程中的关键机制，确保同步器的正常运行并维护网络中节点的一致性。

**优势**：每个节点都可以添加新的区块
**劣势**：相对于raft，通信开销增大，而且最终都要经过主节点，似乎有点得不偿失
