# coding=utf-8
import threading
import time

import toychain
import config

class Miner(threading.Thread):
    def __init__(self, toychain):
        threading.Thread.__init__(self)
        self.toychain = toychain

    def run(self):
        tc = self.toychain
        while True:
            toychain.new_block(tc)
            # TODO lock chain, tx pool for atomic
            # txs = list(self.tx_pool)
            # self.tx_pool = []
            # prev_hash = toychain.hash(self.chain[-1])
            # # TODO get target from chain
            # # TODO unlock chain, tx pool
            # target = config.TARGET
            #
            # header = {
            #     'index': len(self.chain) + 1,
            #     'timestamp': time.time(),
            #     'previous_hash': prev_hash,
            # }
            # nonce = toychain.get_nonce(header, target)
            # header["nonce"] = nonce
            #
            # new_block = header
            # new_block['tx'] = txs
            # self.chain.append(new_block)
            # # TODO broadcast new block to network
