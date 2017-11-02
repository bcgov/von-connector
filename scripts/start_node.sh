#! /bin/bash

NODE_NUM="${1}"

START_PORT=9700

rm -rf .indy/*

# Get ip addresses from docker container names
IP1="$(getent hosts node1 | awk '{ print $1 }')"
IP2="$(getent hosts node2 | awk '{ print $1 }')"
IP3="$(getent hosts node3 | awk '{ print $1 }')"
IP4="$(getent hosts node4 | awk '{ print $1 }')"

init_indy_keys --name node$NODE_NUM --seed 000000000000000000000000000Node$NODE_NUM --force

echo generate_indy_pool_transactions \
    --nodes 4 \
    --clients 5 \
    --nodeNum $NODE_NUM \
    --ips $IP1,$IP2,$IP3,$IP4

generate_indy_pool_transactions \
    --nodes 4 \
    --clients 5 \
    --nodeNum $NODE_NUM \
    --ips "$IP1",$IP2,$IP3,$IP4

echo start_indy_node "node"$NODE_NUM $(( $START_PORT + ( $NODE_NUM * 2 ) - 1 )) $(( $START_PORT + ( $NODE_NUM * 2 ) ))
start_indy_node "node"$NODE_NUM $(( $START_PORT + ( $NODE_NUM * 2 ) - 1 )) $(( $START_PORT + ( $NODE_NUM * 2 ) ))
