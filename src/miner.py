# coding=utf-8
import threading


class Miner(threading.Thread):
    def __init__(self, toychain):
        threading.Thread.__init__(self)
        self.toychain = toychain

    def run(self):
        while True:
            self.toychain.new_block()
