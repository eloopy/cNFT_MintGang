# **cNFT_MintGang**

The cNFT_MintGang is a group of Python and Bash scripts created to help mint Cardano NFT's and Native Tokens.
The scripts follows the process described in the [Cardano Developer Portal](https://developers.cardano.org).
NFT images are uploaded to PINATA automatically so you will need to open an account with them first. 

You will also need cardano-cli and cardano-node installed. You can follow the [Guild Operators Guide](https://cardano-community.github.io/guild-operators/) to get everything up and running.

# **mintNFT.py**
This is the main script for NFT minting. You will have to set your own variables:

tamount

policy_ID

payAddr

payAddr_skey

deadLine_slot

deposit

socketPath

pinFile_endPoint

authToken


# **build.sh**
This scripts builds the raw transaction. Some variables need to be set also:

script

metadata

protocol









