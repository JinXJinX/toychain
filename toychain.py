# coding=utf-8
import time

import requests
import config
import utils


class ToyChain:
    def __init__(self, pvt_key=None, version=config.VERSION):
        # TODO use private variables
        self.tx_pool = []
        self.version = version
        self.nodes = utils.get_nodes()

        self.pvt_key = pvt_key or utils.new_pvt_key()
        self.pub_key = utils.pvt_2_pub_key(self.pvt_key)
        self.address = utils.pub_2_address(self.pub_key)

        self.get_chain()

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
        coinbase_tx = new_tx('0', self.pub_key, 50)
        txs = [coinbase_tx] + self.tx_pool
        # Reset the current list of transactions
        self.tx_pool = []
        # TODO unlock thead

        block = dict(header)
        nonce = utils.get_nonce(header)
        block['nonce'] = nonce
        block['hash'] = utils.hash(block)
        block['tx'] = txs
        chain.append(block)

    def new_tx(self, to_address, amount, fee, signature):
        tx = {
            'from': self.address,
            'to': to_address,
            'total_input': amount + fee,
            'total_output': amount,
            'signature': self._get_signature(),
            'ts': time.time(),
        }
        tx['hash'] = utils.hash(tx)
        # TODO verify tx
        tx['confirmation'] = 1
        return tx

    def _get_signature(self):
        pass

    def get_target(self):
        # TODO adjust target based on previous blocks' mining time
        return config.TARGET

    def get_chain(self):
        if self.nodes:
            chain = []
            height = 0
            node = self.nodes[0]
            while True:
                ret, data = _get(url=f'http://{node}/get_block/{height}')
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


def verify_pvt_key(inp):
    """
    Check input pvt key is a valid format toychain pvt key

    :param inp: str,
    :return: bool
    """
    pass


def verify_chain(chain):
    """
    Check required fields, and caculate whole chain from height 1

    :param chain: list of block data
    :return: bool
    """
    pass


def verify_tx(tx):
    """
    Check required fields, and verify account money and signature

    :param tx: dict, tx data
    :return: bool
    """
    pass


def verify_block(block):
    """
    Check required fields, and verify hash, nonce, and target

    :param block: dict, block data
    :return: bool
    """
    pass


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
