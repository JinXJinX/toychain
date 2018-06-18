# coding=utf-8


class Miner(threading.Thread):
    def __init__(self, chain, tx_pool):
        threading.Thread.__init__(self)
        self.chain = chain
        self.tx_pool = tx_pool

    def run(self):
        pass
