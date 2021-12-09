#!/usr/bin/env PYTHONHASHSEED=6561 python3
#
# Created By  : sk@spacemonk.io
# Created Date: 6th Dec 2021
# Version ='1.0'
#
#  Simulate node methods
#  - Simulate propagation of transactions bypassing network I/O
#  - Rx event process triggered synchronously
#

from transaction import Transaction
from blockchain import Blockchain

def process_transactions(block_chain:Blockchain, txn_obj:Transaction):
    block_chain.add_transactions_to_new_block([txn_obj])

def broadcast_msg(msg_hex):
    msg_bytes = msg_hex.decode("hex")
    broadcast_msg_to_blockchain_nodes(msg_bytes)

def broadcast_txn(block_chain: Blockchain, txn_obj: Transaction, simulate_network = False):
    if simulate_network:
        txn_msg = txn_obj.serialize_to_hex(True, True)
        broadcast_msg(txn_msg)
    else:
        #Bypass network I/O(for now) and trigger rx event processing
        handle_rx_event(block_chain, txn_obj)

def handle_rx_event(block_chain, txn_obj):
    process_transactions(block_chain, txn_obj)


def broadcast_msg_to_blockchain_nodes(msg_bytes):
    #Not implemented for now
    pass
