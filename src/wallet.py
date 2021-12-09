#!/usr/bin/env PYTHONHASHSEED=6561 python3
#
# Created By  : sk@spacemonk.io
# Created Date: 6th Dec 2021
# Version ='1.0'
#
#  Simulate a crypto wallet
#  Using RSA instead of ECDSA. Why? My familiarity with RSA :)
#
import hashlib

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

from transaction import Transaction

# A simple wallet based on RSA algo
class Wallet:
    def __init__(self):
        self.private_key =  RSA.generate(1024)

    def public_key_get(self):
        public_key = self.private_key.publickey()
        return public_key.export_key().decode()

    def public_key_bin(self):
        public_key = self.private_key.publickey()
        pkey_bin = public_key.export_key(format='DER')
        return pkey_bin

    def wallet_address(self):
        return hashlib.sha256(self.public_key_bin()).hexdigest()

    def sign_message_hex(self, message):
        digest = SHA256.new()
        digest.update(message.encode('utf-8'))

        # Sign the message
        signer = PKCS1_v1_5.new(self.private_key)
        sig = signer.sign(digest)
        return sig.hex()

    # Generate signature for transaction involving previous Unspent Transaction Output
    def spend_wallet_balance(self, utxo_id, output_idx, tokens, beneficiary_addr):
        txn_obj = Transaction(utxo_id, output_idx, tokens, beneficiary_addr, self.public_key_bin())
        txn_msg = txn_obj.serialize_to_hex()
        txn_obj.set_sign_hex(self.sign_message_hex(txn_msg))
        return txn_obj
