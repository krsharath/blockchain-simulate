#!/usr/bin/env PYTHONHASHSEED=6561 python3
#
# Created By  : sk@spacemonk.io
# Created Date: 6th Dec 2021
# Version ='1.0'
#
# Tests to validate below use cases
# - store transactions in a distributed ledger
# - detect and prevent data tampering
# - prevent double spending
# - secure against MITM(Man in the middle) attacks
# - secure ownership of transactions for a given wallet address
#

from copy import deepcopy
from blockchain import Blockchain
from node import broadcast_txn
from wallet import Wallet
from transaction import Transaction


class TestClass:
    def test_block_chain(self):
        #Create block Blockchain
        block_chain = Blockchain()

        #Check Genesis block
        assert(len(block_chain.chain) == 1)
        print('Genesis block created')
        #block_chain.dump_blockchain()
        
        #Create generation transaction, credit 100 tokens to the miner Bob
        bob_wallet = Wallet()
        bob_txn = Transaction('ff' * 32, -1, 100, bob_wallet.wallet_address())
        bob_txn.set_generation()
        added = broadcast_txn(block_chain, bob_txn)
        #block_chain.dump_blockchain()
        print('Bob rewarded 100 tokens for mining')
        assert(len(block_chain.chain) == 2)
        assert(block_chain.is_valid())

        #Transfer 100 tokens from Bob to Elsa
        elsa_wallet = Wallet()
        utxo_id = bob_txn.hash_id
        bob_to_elsa_txn = bob_wallet.spend_wallet_balance(utxo_id, 0, 95, elsa_wallet.wallet_address())
        broadcast_txn(block_chain, bob_to_elsa_txn)
        assert(len(block_chain.chain) == 3)
        elsa_utxo_id = bob_to_elsa_txn.hash_id
        assert(block_chain.is_valid())
        print('Bob transferred 95 tokens to Elsa')
        #block_chain.dump_blockchain()

        #Try double spending same transaction
        bob_to_elsa_txn_duplicate = deepcopy(bob_to_elsa_txn)
        broadcast_txn(block_chain, bob_to_elsa_txn_duplicate)
        assert(len(block_chain.chain) == 3)
        print('Transaction Error:', bob_to_elsa_txn_duplicate.err_msg)

        #Man in the middle atttack - replace recipient's wallet address
        #Elsa wants to transfer 100 tokens to Ram
        ram_wallet = Wallet()
        elsa_to_ram_txn = elsa_wallet.spend_wallet_balance(elsa_utxo_id, 0, 90, ram_wallet.wallet_address())

        #James intercepts the frame and puts his wallet address instead
        james_fraud_txn = deepcopy(elsa_to_ram_txn)
        james_wallet = Wallet()
        james_fraud_txn.rx_address = james_wallet.wallet_address()
        broadcast_txn(block_chain, james_fraud_txn)
        assert(len(block_chain.chain) == 3)
        print('Transaction Error:', james_fraud_txn.err_msg)

        #James tries to spend using his wallet, but utxo_id pointing to Elsa's
        james_wallet2 = Wallet()
        james_fraud_txn = james_wallet.spend_wallet_balance(elsa_utxo_id, 0, 80, james_wallet2.wallet_address())
        broadcast_txn(block_chain, james_fraud_txn)
        assert(len(block_chain.chain) == 3)
        print('Transaction Error:', james_fraud_txn.err_msg)

        #the original elsa->ram transaction will go through
        broadcast_txn(block_chain, elsa_to_ram_txn)
        assert(len(block_chain.chain) == 4)
        print('Elsa transferred 90 tokens to Ram')
        ram_utxo_id = elsa_to_ram_txn.hash_id

        #Ram tries to transfer 150 tokens to Ali, 50 tokens more than what he is legally allowed to
        ali_wallet = Wallet()
        ram__to_ali_txn = ram_wallet.spend_wallet_balance(ram_utxo_id, 0, 150, ali_wallet.wallet_address())
        broadcast_txn(block_chain, ram__to_ali_txn)
        assert(len(block_chain.chain) == 4)
        print('Transaction Error:', ram__to_ali_txn.err_msg)
        block_chain.dump_blockchain()
