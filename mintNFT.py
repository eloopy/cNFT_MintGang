#!/usr/bin/python3

import os
import re
import sys
import requests
import json
import subprocess
import time
import hashlib


nftFilePath = ""
nftFileName = ""
tname=""
tnameHex=""
tcolor=""
tpattern=""
twallet=""
ipfsHash=""
UTxO=""
balance = ""



tamount="1"
policy_ID = "Policy ID HERE"
#Description and traits
tpublisher=""
tdescipt = ""
tstyle = ""
#------------------
payAddr= "PAYMENT ADDRESS"
payAddr_skey = 'PAYMENT SKEY PATH HERE'
deadLine_slot = "SLOT NUMBER"
deposit="LOCK FUNDS"



socketPath="YOUR SOCKET PATH HERE"

pinFile_endPoint = "PINATA ENDPOINT"
authToken='PINATA AUTH TOKEN'



#===================================== FUNCTIONS =============================================

def save_to_file(file_name, content):
        try:
           with open(file_name, 'w') as jf:
              jf.write(content)
              
           return True
        except Exception as e:
           print(e)    


def getBalance():
        rawUtxoTable = subprocess.check_output([ \
                         '/home/ubuntu/.cabal/bin/cardano-cli', \
                         'query', 'utxo', '--mainnet','--address',payAddr], \
                         env={'CARDANO_NODE_SOCKET_PATH': socketPath})



        utxoTableRows = rawUtxoTable.strip().splitlines()
        balance = ""
        addrHash = ""
        addrIndex = ""
        
        for x in range(2, len(utxoTableRows)):
                cells = utxoTableRows[x].split()
                balance =  cells[2].decode("utf-8")
                addrHash = cells[0].decode("utf-8")
                addrIndex = cells[1].decode("utf-8")

        return addrHash, addrIndex, balance
        

        
        

#==================================================================================================


os.system('clear')
print("\033[96m========== Cardano NFT Mint Machine v2.0 ===========\033[0m" + "\n")


for file in os.listdir("."):
    if file.endswith(".png"):
        nftFileName = file
        nftFilePath = os.path.join(os.getcwd(),file)
      
if nftFilePath == "":
    print("\033[91mNo NFT image file found.\033[0m" + "\n")
    exit()

#print('Uploding file to IPFS... ')    


f = open(nftFilePath, 'rb')
files = {'file': (nftFileName,f, 'text/plain')}
body, content_type = requests.models.RequestEncodingMixin._encode_files(files, {})
header = {'Content-Type': content_type, 'Authorization': 'Bearer ' + authToken}

r = requests.post(pinFile_endPoint,data=body,headers=header)

if (r.status_code == 200):
   
            jsonRes = json.loads(r.text)
            ipfsHash = jsonRes["IpfsHash"]
            f.close()
            print("\033[92mFile uploaded to IPFS: \033[0m" + ipfsHash + "\n")

else:
            print("\033[91mError uploading file to IPFS.\033[0m" + "\n")
            f.close()
            exit()

#=================================================================================================


tname = input("\033[92m" +"Enter Token Name:" + "\033[0m")
utf_name = tname.encode('utf-8')
tnameHex =(utf_name.hex())

tcolor = input("\033[92m" + "Enter Color:" + "\033[0m")
tpattern = input("\033[92m" + "Enter Patter:" + "\033[0m")

twallet = input("\033[92m" + "Enter Destination Wallet:" + "\033[0m")

#=======================================================================================================

result = subprocess.run([ \
                         '/home/ubuntu/.cabal/bin/cardano-cli', \
                         'query', 'protocol-parameters', '--mainnet','--out-file','protocol.json'], \
                         env={'CARDANO_NODE_SOCKET_PATH': socketPath}, \
                         capture_output=True, encoding='UTF-8')

#print(result.stdout)
#print(result.stderr)  

#=======================================================================================================



ipfsHash_addr = 'ipfs://' + ipfsHash
tmpWF_1 = os.getcwd() +  '/metadata.json'
            
metadata = '{"721":{"'+policy_ID+'":{"'+tname+'":{"image":"'+ ipfsHash_addr+'","Publisher": "'+tpublisher+'",'+tdescipt+','+tstyle+',"Colors": "'+tcolor+'","Pattern Size": "'+tpattern+'"}}}}' 
            
            
if (save_to_file(tmpWF_1,metadata)):

            print('\n')         
            #print('\033[92mmetadata.json saved\033[0m' + '\n') 
else:
            print('\033[91mERROR==> metadata.json could not be saved\033')   
            exit()


hash, index, balance = getBalance()
UTxO = hash + '#' + index


#===================================================================================            
                     
        
result = subprocess.run(['./build.sh',UTxO,twallet,tamount,policy_ID,tnameHex,deadLine_slot,balance,payAddr],capture_output=True, encoding='UTF-8')
         
print(result.stdout)
print(result.stderr)
 

#===================================================================================

tmpWF_2 = 'policy.skey'
tmpWF_3 = 'TX.raw'
tmpWF_4 = 'TX.sign'
            
result = subprocess.run([ \
                         '/home/ubuntu/.cabal/bin/cardano-cli', \
                         'transaction', 'sign', \
                         '--mainnet', \
                         '--signing-key-file',payAddr_skey, \
                         '--signing-key-file',tmpWF_2, \
                         '--tx-body-file',tmpWF_3, \
                         '--out-file',tmpWF_4], \
                         env={'CARDANO_NODE_SOCKET_PATH': socketPath}, \
                         capture_output=True, encoding='UTF-8')  

print(result.stdout)
print(result.stderr)


#===================================================================================


if input("\033[92m" + "Ready to mint... Are you sure? (y/n):" + "\033[0m") == "n": exit()
print("\n")


#===================================================================================


tmpWF_1 = 'TX.sign'
            
result = subprocess.run([ \
                        '/home/ubuntu/.cabal/bin/cardano-cli', \
                        'transaction', 'submit', \
                        '--tx-file',tmpWF_1, \
                        '--mainnet'], \
                        env={'CARDANO_NODE_SOCKET_PATH': socketPath}, \
                        capture_output=True, encoding='UTF-8')      
                  
                          
            
            
print(result.stdout)
print(result.stderr)



#===================================================================================


os.system("rm *.png")
os.system("rm *.json")
os.system("rm *.raw")
os.system("rm *.sign")


#print('\033[92mFiles cleared\033[0m' + '\n') 
print('\033[92mAll done!\033[0m' + '\n') 

exit()





           