# Blockchain Simulator
A simple blockchain simulator in Python

## Overview
Understanding CryptoCurrency involves understanding two concepts
- Blockchain
- Cryptography

This is a simple implementation to show how *Blockchain and Crypto Software* can be used to
 - store transactions in a distributed ledger
 - detect and prevent data tampering
 - prevent double spending
 - secure against MITM(Man in the middle) attacks
 - secure ownership of transactions for a given wallet address

## Why simulate? Why not look at real code?
- Simpler code base (1/100th), environment(single venv instance vs multiple docker instances)
- Faster and Easier to experiment (few minutes vs few hours/days)

## How can I setup?
- Install venv and python packages
```
python3 -m venv bcenv
source bcenv/bin/activate
pip install -r requirements.txt 
```

## Testing?
Few tests are implemented in test/test_blockchain.py. (create blockchain, record transactions, double spending, relay attack) 

You can run these tests using below command
```
PYTHONPATH=src  python -m pytest test/test_blockchain.py -s
 
   Sample Output:
   
test/test_blockchain.py Genesis block created
Bob rewarded 100 tokens for mining
Bob transferred 95 tokens to Elsa
Transaction Error: Double Spending
Transaction Error: Signature Verification Failed
Transaction Error: UTXO address<->PubKey mismatch
Elsa transferred 90 tokens to Ram
Transaction Error: Insufficient Balance
************Chain Start****************
Block: 0
Hash 0042a5dfb16676e77b2c24aa5db6b3f4949775e35795e551349017f7e4f2bd0b
Prev Hash 0
Nonce 31
Transactions:
	Genesis Transaction
	Transaction Hash 513c6adb6e00b0cc27bf2747b9aad6c3b41b0e37f8b8bea4d5de705e359e5a7a
	Tokens Received 0
	Rx Address 0000000000000000000000000000000000000000000000000000000000000000

Block: 1
Hash 000cf429d4221399ff0de7cdd6c82d3c344a47ac03d247531bf03c843df1222b
Prev Hash 0042a5dfb16676e77b2c24aa5db6b3f4949775e35795e551349017f7e4f2bd0b
Nonce 329
Transactions:
	Transaction Hash f815b14c4d02b9f5a0e1e8ec62aa362805e995f2b1fdcb74c3c7c7643c905d49
	Tokens Received 100
	Rx Address 9e288b48a7152c65d1b5e086276e8ac1b73d7c685f1817905476c0296d5d7b89

Block: 2
Hash 00b8b34e99554027187e5ed745d0c4c1f1407f578ad0fd840ee2a9205c0d4bae
Prev Hash 000cf429d4221399ff0de7cdd6c82d3c344a47ac03d247531bf03c843df1222b
Nonce 320
Transactions:
	Transaction Hash d4bfce4d008219c0d43fb2678531d814ef3b8404fd7fd5df3eb5496bed0d4c86
	Tokens Received 95
	Rx Address 3bfe1202cb62e130ac3d38f1e1d1221f554a069d6890b39c96f20555d1c121ba

Block: 3
Hash 0004f34fe06160537a27a0701e0fcab5928a654b8b7ed59abb62c8aea5ae07cb
Prev Hash 00b8b34e99554027187e5ed745d0c4c1f1407f578ad0fd840ee2a9205c0d4bae
Nonce 331
Transactions:
	Transaction Hash 637e4ccabbf79bf0b972834ce3c908cc7c07365e2a1f802f37696569a86373ac
	Tokens Received 90
	Rx Address 81ca453f729067146ce49e76eda1e1742acf9c36e9dcf46af9374172b2cbca0a

************Chain End******************
```
   


