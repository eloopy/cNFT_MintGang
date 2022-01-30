#!/bin/bash 
export CARDANO_NODE_SOCKET_PATH=/opt/cardano/cnode/sockets/node0.socket

script="policy.script"
metadata="metadata.json"
protocol="protocol.json"
outputF="TX.raw"
outputFF="TXfinal.raw"

txIN=$1
taddress=$2
tokenamount=$3
policyid=$4
tokenname=$5
slot=$6
funds=$7
paddress=$8


deposit=2000000


/home/ubuntu/.cabal/bin/cardano-cli transaction build \
--mainnet \
--alonzo-era \
--tx-in $txIN \
--tx-out $taddress+$deposit+"$tokenamount $policyid.$tokenname" \
--change-address $paddress \
--mint="$tokenamount $policyid.$tokenname" \
--minting-script-file $script \
--metadata-json-file $metadata  \
--invalid-hereafter $slot \
--witness-override 2 \
--out-file $outputF



