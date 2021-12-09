#!/usr/bin/env PYTHONHASHSEED=6561 python3
#
#
# Created By  : sk@spacemonk.io
# Created Date: 6th Dec 2021
# Version ='1.0'
#
# Implementation to simulate Blockchain transaction:
# Transaction objects are created by Wallet Software, propagated
# through the network to blockchain nodes, verifed and added into a
# newly mined block.
#

import binascii
import hashlib

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5


# A simple transaction
class Transaction:
    def __init__(self, utxo_id, output_idx, tokens, rx_address, pub_key=None):
        self.utxo_id = utxo_id
        self.output_idx = output_idx
        self.tokens = tokens
        self.rx_address = rx_address
        self.pubkey = pub_key
        self.hash_id = self.get_hash()

        # Not signed yet
        self.sign_hex = None
        self.err_msg = None

        # Not a generation transaction, by default
        self.generation = False
        self.genesis = False

    def serialize_to_hex(self, include_signature=False, include_pubkey=False):
        # Assume message format [32 byte Tx ID][4 byte Output Idx][4 byte tokens][32 byte rx_addr]
        txn_msg = self.utxo_id + hex(self.output_idx)[2:].zfill(8) + \
                  hex(self.tokens)[2:].zfill(8) + self.rx_address

        if include_signature and self.sign_hex:
            txn_msg = txn_msg + self.sign_hex

        if include_pubkey:
            txn_msg = txn_msg + binascii.hexlify(self.pubkey)

        return txn_msg

    def set_generation(self):
        self.generation = True

    def set_genesis(self):
        self.genesis = True

    def set_sign_hex(self, sign):
        self.sign_hex = sign

    def pub_key_hash(self):
        if not self.pubkey:
            return None

        return hashlib.sha256(self.pubkey).hexdigest()

    def get_hash(self):
        txn_msg = self.serialize_to_hex().encode()
        return hashlib.sha256(txn_msg).hexdigest()

    def verify_signature(self):
        if not self.sign_hex:
            return False

        txn_msg = self.serialize_to_hex()
        digest = SHA256.new()
        digest.update(txn_msg.encode('utf-8'))
        sigbin = bytes.fromhex(self.sign_hex)

        public_key = RSA.importKey(self.pubkey)
        verifier = PKCS1_v1_5.new(public_key)
        verified = verifier.verify(digest, sigbin)
        return verified

    def set_failure_message(self, msg):
        self.err_msg = msg

    def dump(self):
        if self.genesis:
            print('\tGenesis Transaction')

        print('\tTransaction Hash', self.hash_id)
        print('\tTokens Received', self.tokens)
        print('\tRx Address', self.rx_address, '\n')


def get_genesis_transaction():
    rx_addr = '0' * 64
    hash_id = 'ff' * 32
    tokens = 0
    output_idx = -1
    genesis_transaction = Transaction(hash_id, output_idx, tokens, rx_addr)
    genesis_transaction.set_genesis()
    return genesis_transaction
