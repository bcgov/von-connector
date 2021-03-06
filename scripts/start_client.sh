#! /bin/bash

# Get ip addresses from docker container names
IP1="$(getent hosts node1 | awk '{ print $1 }')"
IP2="$(getent hosts node2 | awk '{ print $1 }')"
IP3="$(getent hosts node3 | awk '{ print $1 }')"
IP4="$(getent hosts node4 | awk '{ print $1 }')"

echo generate_indy_pool_transactions \
    --nodes 4 \
    --clients 1 \
    --ips $IP1,$IP2,$IP3,$IP4

generate_indy_pool_transactions \
    --nodes 4 \
    --clients 1 \
    --ips "$IP1",$IP2,$IP3,$IP4

indy
