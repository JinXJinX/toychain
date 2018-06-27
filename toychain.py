# coding=utf-8
import time

from Crypto.PublicKey import RSA
import requests
import settings
import utils
import verifier as vf


class ToyChain:
    def __init__(self, port, pvt_key=None,
                 version=settings.VERSION, node=True):
        # TODO use private variables
        self.tx_pool = []
        self.version = version
        self.port = port
        self.nodes = utils.get_nodes(port)

        self.pvt_key = utils.new_rsa_key(pvt_key)
        self.pub_key = self.pvt_key.publickey().exportKey().decode()
        self.address = utils.pub_2_address(self.pub_key)

        if node:
            self.ledger = {}
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
        # TODO unlock thead

        block = dict(header)
        nonce = utils.get_nonce(header)
        block['nonce'] = nonce
        block['hash'] = utils.get_hash(block)
        block['tx'] = txs
        block['confirmation'] = 1
        chain.append(block)
        self.broadcast('block', block)

        # update coinbase reward on ledger after fount the block
        if not self.update_ledger([coinbase_tx]):
            print('update ledger error???')
            return

    def send_coin(self, to_address, amount, fee):
        tx = self.new_tx(self.address, to_address, amount, fee)
        tx['hash'] = utils.get_hash(tx)
        tx['signature'] = str(self.pvt_key.sign(tx['hash'].encode(), '')[0])
        tx['pub_key'] = self.pub_key
        tx['confirmation'] = 1

        if not self.update_ledger([tx]):
            return False

        self.tx_pool.append(tx)
        # boradcast tx
        self.broadcast('tx', tx)
        return True

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

    def update_ledger(self, txs, ledger=None):
        ledger = ledger or self.ledger
        for tx in txs:
            if tx['from'] != '0':
                if ledger.get(tx['from'], 0) < tx['total_input']:
                    return False
                ledger[tx['from']] = ledger.get(tx['from']) - tx['total_input']

            ledger[tx['to']] = ledger.get(tx['to'], 0) + tx['total_output']

        return True

    def get_chain_from_node(self, node):
        chain = []
        ledger = {}
        height = 0
        while True:
            ret, data = utils._get(url=f'http://{node}/get_block/{height}')
            if ret and data['ok']:
                block = data.get('block', {})
                if not vf.block(block):
                    break
                if chain and chain[-1]['hash'] != block['prev_hash']:
                    break

                # update ledger
                if not self.update_ledger(block['tx'], ledger):
                    break

                chain.append(block)
                height += 1

            else:
                break
        return chain, ledger

    def init_chain(self):
        for node in self.nodes:
            chain, ledger = self.get_chain_from_node(node)
            if chain:
                self.chain = chain
                self.ledger = ledger
                return

        # Create the genesis block
        print('mining first block')
        self.chain = []
        self.ledger = {}
        self.new_block()

    def broadcast(self, type, data):
        """
        Broadcast data to nodes

        :param nodes: list of nodes
        :param type: str, 'tx', 'block', or 'node'
        :param data: a dict, depends on type,
        """
        data = {type: data}
        for node in list(self.nodes):
            url = f'http://{node}/add_{type}'
            ret, data = utils._post(url=url, json=data)
            if not ret:
                self.nodes.remove(node)

    def add_node(self, node):
        if node in self.chain:
            return True

        self.broadcast('node', node)
        self.nodes.append(node)
        return True

    def add_block(self, new_block):
        # TODO verify block
        if not vf.block(new_block):
            return False

        for block in list(self.chain):
            if block['hash'] == new_block['hash']:
                block['confirmation'] += 1
                return True
        self.chain.append(new_block)
        self.broadcast('block', new_block)
        return True

    def add_tx(self, new_tx):
        if not vf.tx(new_tx):
            return False

        # TODO modify amounts' money
        if not self.update_ledger([new_tx]):
            return False

        for tx in list(self.tx_pool):
            if tx['hash'] == new_tx['hash']:
                tx['confirmation'] += 1
                return
        self.tx_pool.append(new_tx)
        self.broadcast('tx', new_tx)
        return True

    def get_nodes(self):
        return list(self.nodes)

    def get_chain(self):
        return list(self.chain)

    def get_tx_pool(self):
        return list(self.tx_pool)

    def get_pvt_key(self):
        return self.pvt_key.exportKey().decode()

    def get_address(self):
        return self.address

    def get_ledger(self):
        return dict(self.ledger)


def resolve_conflicts():
    pass
