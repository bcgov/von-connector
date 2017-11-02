# VON Connector

Verifiable Organization Network Connector

## Getting Set Up

First, install Docker. Download the installer for your operating system [here](https://store.docker.com/search?type=edition&offering=community). Once it is installed, keep the Docker daemon running in the background.

Once Docker has been installed, open a terminal session and clone this repository:

```bash
git clone <repository url> von-connector
```

Move to the new directory:

```bash
cd von-connector
```

Now you can build the Dockerfile into an image which we will use to run containers (this process will take several minutes):

```bash
./manage build
```

Once the build process completes, you can test the build to make sure everything works properly:

```bash
./manage start_nodes
```

Once the nodes are all running and have connected to each other, you can run the Indy client to test the connection in a separate terminal window:

```bash
./manage start_client
```

The Indy CLI should boot up and you should see the following:

```
Indy-CLI (c) 2017 Evernym, Inc.
Type 'help' for more information.
Running Indy 1.1.159

indy>
```

Now connect to our new Indy network to make sure network is running correctly:

```
connect test
```

What you should see is:

```
indy> connect test
New wallet Default created
Active wallet set to "Default"
Active wallet set to "Default"
Client indy9f7060 initialized with the following node registry:
    Node1C listens at 172.21.0.2 on port 9702
    Node2C listens at 172.21.0.5 on port 9704
    Node3C listens at 172.21.0.3 on port 9706
    Node4C listens at 172.21.0.4 on port 9708
Active client set to indy9f7060
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ listening for other nodes at 0.0.0.0:6001
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ looking for Node1C at 172.21.0.2:9702
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ looking for Node2C at 172.21.0.5:9704
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ looking for Node3C at 172.21.0.3:9706
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ looking for Node4C at 172.21.0.4:9708
Connecting to test...
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node1C
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node2C
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node3C
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node4C
CATCH-UP: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ completed catching up ledger 0, caught up 0 in total
Connected to test.
```

**Specifically**:

```
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node1C
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node2C
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node3C
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node4C
...
Connected to test.
```

If you see this, congratulations! Your nodes are running correctly and you have a connection to the network.

## Running the VON Connector

Start the Indy nodes:

```bash
./manage start_nodes
```

Once that completes, start the VON Connector in a separate terminal window:

```bash
./manage start_von_connector
```

It will first take a minute to bootstrap the environment and once that completes you should see something like this:

```
Opening pool...



 INFO|command_executor              |                src/commands/mod.rs:71  | Worker thread started
 INFO|indy::commands                |                src/commands/mod.rs:107 | PoolCommand command received
 INFO|pool_command_executor         |               src/commands/pool.rs:54  | Create command received
_indy_loop_callback: Function returned None
 INFO|indy::commands                |                src/commands/mod.rs:107 | PoolCommand command received
 INFO|pool_command_executor         |               src/commands/pool.rs:62  | Open command received
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node1 po
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "{\"op\":\"LEDGER_STATUS\",\"txnSeqNo\":4,\"merkleRoot\":\"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg\",\"ledgerId\":0,\"ppSeqNo\":null,\"viewNo\":null}"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node3 po
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "{\"op\":\"LEDGER_STATUS\",\"txnSeqNo\":4,\"merkleRoot\":\"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg\",\"ledgerId\":0,\"ppSeqNo\":null,\"viewNo\":null}"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node1 {"ppSeqNo":null,"txnSeqNo":4,"op":"LEDGER_STATUS","ledgerId":0,"viewNo":null,"merkleRoot":"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg"}
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node2 po
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "{\"op\":\"LEDGER_STATUS\",\"txnSeqNo\":4,\"merkleRoot\":\"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg\",\"ledgerId\":0,\"ppSeqNo\":null,\"viewNo\":null}"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node4 po
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "{\"op\":\"LEDGER_STATUS\",\"txnSeqNo\":4,\"merkleRoot\":\"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg\",\"ledgerId\":0,\"ppSeqNo\":null,\"viewNo\":null}"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node2 {"ppSeqNo":null,"viewNo":null,"merkleRoot":"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg","ledgerId":0,"txnSeqNo":4,"op":"LEDGER_STATUS"}
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node3 {"ppSeqNo":null,"ledgerId":0,"merkleRoot":"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg","viewNo":null,"op":"LEDGER_STATUS","txnSeqNo":4}
 INFO|indy::commands                |                src/commands/mod.rs:107 | PoolCommand command received
 INFO|indy::commands::pool          |               src/commands/pool.rs:66  | OpenAck handle 1, result Ok(2)
_indy_loop_callback: Function returned 2



Finished opening pool






Closing pool...



 INFO|indy::commands                |                src/commands/mod.rs:107 | PoolCommand command received
 INFO|pool_command_executor         |               src/commands/pool.rs:81  | Close command received
 INFO|pooltest                      |           src/services/pool/mod.rs:792 | Drop started
 INFO|pooltest                      |           src/services/pool/mod.rs:800 | Drop wait worker
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 WARN|indy::services::pool          |           src/services/pool/mod.rs:146 | unhandled msg LedgerStatus(LedgerStatus { txnSeqNo: 4, merkleRoot: "EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg", ledgerId: 0, ppSeqNo: None, viewNo: None })
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node1 po
 WARN|indy::services::pool          |           src/services/pool/mod.rs:146 | unhandled msg Pong
 INFO|pooltest                      |           src/services/pool/mod.rs:803 | Drop finished
 INFO|indy::commands                |                src/commands/mod.rs:107 | PoolCommand command received
 INFO|pool_command_executor         |               src/commands/pool.rs:85  | CloseAck command received
_indy_loop_callback: Function returned None
 INFO|indy::commands                |                src/commands/mod.rs:107 | PoolCommand command received
 INFO|pool_command_executor         |               src/commands/pool.rs:58  | Delete command received
_indy_loop_callback: Function returned None



Finished closing pool
```

The VON Agent has connected to the network!
