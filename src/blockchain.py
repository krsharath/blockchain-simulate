#!/usr/bin/env PYTHONHASHSEED=6561 python3
#
# Created By  : sk@spacemonk.io
# Created Date: 6th Dec 2021
# Version ='1.0'
#
# Understanding CryptoCurrency involves understanding two concepts
# - Blockchain
# - Cryptography
#
# This is a simple implementation to show how *Blockchain and Crypto Software* can be used to
# - store transactions in a distributed ledger
# - detect and prevent data tampering
# - prevent double spending
# - secure against MITM(Man in the middle) attacks
# - secure ownership of transactions for a given wallet address
#

import hashlib
from transaction import Transaction, get_genesis_transaction


# A simple block
class Block:
    def __init__(self, prev_hash, transactions):
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        hash_str = self.prev_hash + str(self.transactions) + str(self.nonce)
        return hashlib.sha256(hash_str.encode()).hexdigest()

    def mine_block(self, difficulty):
        prefix_str = '0' * difficulty
        while True:
            if self.hash.startswith(prefix_str):
                break

            self.nonce = self.nonce + 1
            self.hash = self.compute_hash()

    def dump_block(self):
        print('Hash', self.hash)
        print('Prev Hash', self.prev_hash)
        print('Nonce', self.nonce)
        print('Transactions:')
        for transaction in self.transactions:
            transaction.dump()


# A chain of blocks
class Blockchain:
    def __init__(self, difficulty = 2):
        genesis_transaction = get_genesis_transaction()
        genesis_block = Block('0', [
            genesis_transaction
        ])
        self.difficulty = difficulty
        genesis_block.mine_block(self.difficulty)
        self.chain = [genesis_block]

    def create_new_block(self, new_transactions):
        last_block = self.chain[-1]
        new_block = Block(last_block.hash, new_transactions)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def get_all_commited_transactions(self):
        txns = []
        for idx in range(1, len(self.chain)):
            current_block = self.chain[idx]
            txns = current_block.transactions + txns

        return txns

    def add_transactions_to_new_block(self, transactions:[Transaction]):
        #Get all commited txns
        commited_txns = self.get_all_commited_transactions()

        #Get all Commited transaction HASHes
        commited_txn_dict = {tx.hash_id:tx for tx in commited_txns}

        #Get all spent transaction HASHes
        spent_utx_list = [tx.utxo_id for tx in commited_txns]

        valid_txns = self.verify_transactions(transactions,
                                              commited_txn_dict, spent_utx_list)
        if valid_txns:
            self.create_new_block(valid_txns)
        return len(valid_txns)

    def verify_transactions(self, transactions, commited_txn_dict, spent_utx_list):
        valid_txns = []
        #Validate each transaction
        for transaction in transactions:
            if transaction.generation is True:
                valid_txns.append(transaction)
                continue

            #Is this authentic transaction?
            if not transaction.verify_signature():
                transaction.set_failure_message('Signature Verification Failed')
                continue

            utxo_id = transaction.utxo_id
            if utxo_id in spent_utx_list:
                transaction.set_failure_message('Double Spending')
                continue

            if utxo_id in commited_txn_dict:
                utxo_txn = commited_txn_dict[utxo_id]
                #verify if pubkey hash matches utxo wallet address
                if utxo_txn.rx_address == transaction.pub_key_hash():
                    #verify tokens are within bounds
                    if utxo_txn.tokens >= transaction.tokens:
                        #All good...
                        valid_txns.append(transaction)
                        spent_utx_list.append(transaction.utxo_id)
                    else:
                        transaction.set_failure_message('Insufficient Balance')
                else:
                    transaction.set_failure_message('UTXO address<->PubKey mismatch')

        return valid_txns

    def is_valid(self):
        for idx in range(1, len(self.chain)):
            prev_block = self.chain[idx - 1]
            current_block = self.chain[idx]

            if current_block.compute_hash() != current_block.hash:
                return False

            if current_block.prev_hash != prev_block.hash:
                return False

        return True

    def dump_blockchain(self):
        print('************Chain Start****************')
        for idx,block in enumerate(self.chain):
            print('Block:', idx)
            block.dump_block()
        print('************Chain End******************\n')
