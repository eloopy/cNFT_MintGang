#!/bin/bash


clear
export CARDANO_NODE_SOCKET_PATH=/opt/cardano/cnode/sockets/node0.socket


realtokenname="Tpken name in text format"
tokenamount="Token amount here"
DestAddr="Destination address here"
slotnumber="Slot number here"

payAddr=""
UTxO=""
paymentskey="Payment skey path here"
policyid=$(cat policy/policyID)
deposit="lock funds here"


tokenname=$(echo -n $realtokenname | xxd -b -ps -c 80 | tr -d '\n')


/home/ubuntu/.cabal/bin/cardano-cli transaction build  \
--mainnet \
--alonzo-era \
--tx-in $UTxO \
--tx-out $DestAddr+$deposit+"$tokenamount $policyid.$tokenname" \
--change-address $payAddr \
--mint="$tokenamount $policyid.$tokenname" \
--minting-script-file policy/policy.script \
--invalid-hereafter $slotnumber \
--witness-override 2 \
--out-file matx.raw

echo 

read -p "Ready to mint...Are you sure? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Exit"
    exit 1
fi

/home/ubuntu/.cabal/bin/cardano-cli transaction sign  \
--mainnet \
--signing-key-file $paymentskey  \
--signing-key-file policy/policy.skey  \
--tx-body-file matx.raw  \
--out-file matx.signed

/home/ubuntu/.cabal/bin/cardano-cli transaction submit --tx-file matx.signed --mainnet



rm *.raw
rm *.signed

echo 
echo "All done!"
echo 


