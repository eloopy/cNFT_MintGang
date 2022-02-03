#!/bin/bash 

UTxOA="UTxO containg the tokens"
UTxOB="UTxO for payment"
address="Wallet address"
burnoutput=2000000
policyid="POLICY ID HERE"
realtokenname="Token name in text format"
slot=88777888
paymentskey="payment skey path here"

export CARDANO_NODE_SOCKET_PATH="YOUR SOCKET PATH HERE"





clear

tokenname=$(echo -n $realtokenname | xxd -b -ps -c 80 | tr -d '\n')


touch burning.raw && touch burning.signed
chown ubuntu burning.raw && chown ubuntu burning.signed

/home/ubuntu/.cabal/bin/cardano-cli transaction build \
 --mainnet \
 --alonzo-era \
 --tx-in $UTxOA \
 --tx-in $UTxOB \
 --tx-out $address+$burnoutput \
 --mint="-1 $policyid.$tokenname" \
 --minting-script-file policy.script \
 --change-address $address \
 --invalid-hereafter $slot \
 --witness-override 2 \
 --out-file burning.raw
 
 
 /home/ubuntu/.cabal/bin/cardano-cli transaction sign  \
 --signing-key-file $paymentskey  \
 --signing-key-file policy.skey \
 --mainnet  \
 --tx-body-file burning.raw \
 --out-file burning.signed

 echo 

read -p "Ready to burn...Are you sure? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi
 
 /home/ubuntu/.cabal/bin/cardano-cli transaction submit --tx-file burning.signed --mainnet
 
 rm burning.raw && rm burning.signed
 echo All done!
 


 
 
 
 
 
