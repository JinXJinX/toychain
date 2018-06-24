# coding=utf-8
import time

from Crypto.PublicKey import RSA
import requests
import settings
import utils


class ToyChain:
    def __init__(self, port, pvt_key=None, version=settings.VERSION):
        # TODO use private variables
        self.tx_pool = []
        # self.chain = []
        self.version = version
        self.port = port
        self.nodes = utils.get_nodes(port)

        self.pvt_key = pvt_key or utils.new_rsa_key()
        self.pub_key = self.pvt_key.publickey().exportKey().decode()
        self.address = utils.pub_2_address(self.pub_key)

        self.init_chain()

    def new_block(self):
        chain = self.chain
        header = {
            'version': self.version,
            'ts': time.time(),
            'prev_hash': '' if not chain else chain[-1]['hash'],
            'nonce': '0',
            'target': self.get_target(),
            # TODO merkle root
        }
        # TODO does the coinbase tx affects merkle root?
        # TODO lock thead
        coinbase_tx = self.new_tx('0', self.address, 50, 0)
        tx_pool = self.tx_pool
        txs = [coinbase_tx] + [tx_pool.pop(0) for _ in range(len(tx_pool))]
        # Reset the current list of transactions
        # self.tx_pool = []
        # TODO unlock thead

        block = dict(header)
        nonce = utils.get_nonce(header)
        block['nonce'] = nonce
        block['hash'] = utils.get_hash(block)
        block['tx'] = txs
        block['confirmation'] = 1
        chain.append(block)
        self.broadcast('block', block)

    def send_coin(self, to_address, amount, fee):
        tx = self.new_tx(self.address, to_address, amount, fee)
        tx['hash'] = utils.get_hash(tx)
        tx['signature'] = str(self.pvt_key.sign(tx['hash'].encode(), '')[0])
        tx['pub_key'] = self.pub_key
        tx['confirmation'] = 1
        self.tx_pool.append(tx)
        # TODO boradcast tx
        self.broadcast('tx', tx)

    def new_tx(self, from_address, to_address, amount, fee):
        tx = {
            'from': from_address,
            'to': to_address,
            'total_input': amount + fee,
            'total_output': amount,
            'ts': time.time(),
        }
        return tx

    def get_target(self):
        # TODO adjust target based on previous blocks' mining time
        return settings.TARGET

    def init_chain(self):
        if self.nodes:
            chain = []
            height = 0
            node = self.nodes[0]
            while True:
                ret, data = utils._get(url=f'http://{node}/get_block/{height}')
                if ret and data['ok']:
                    chain.append(data['block'])
                    height += 1
                else:
                    break
            if chain:
                self.chain = chain
                return

        # Create the genesis block
        print('mining first block')
        self.chain = []
        self.new_block()

    def broadcast(self, type, data):
        data = {type: data}
        for node in list(self.nodes):
            url = f'http://{node}/add_{type}'
            ret, data = utils._post(url=url, json=data)
            print(ret, data)
            if not ret:
                self.nodes.remove(node)

    def add_node(self, node):
        self.nodes.append(node)

    def add_block(self, block):
        print(block)
        # TODO verify block
        for b in self.chain:
            if b['hash'] == block['hash']:
                b['confirmation'] += 1
                return
        self.chain.append(block)
        self.broadcast('block', block)
        return

    def get_nodes(self):
        return list(self.nodes)

    def get_chain(self):
        return list(self.chain)

    def get_tx_pool(self):
        return list(self.tx_pool)


def resolve_conflicts():
    pass


def post_data(nodes, type, data):
    """
    Broadcast data to nodes

    :param nodes: list of nodes
    :param type: str, 'tx', 'block', or 'node'
    :param data: a dict, depends on type,
    """
    postfix = f'/add_{type}'
    for node in nodes:
        r = requests.post(url, data)
