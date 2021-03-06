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
        self.ledger = {}

        self.pvt_key = utils.new_rsa_key(pvt_key)
        self.pub_key = self.pvt_key.publickey().exportKey().decode()
        self.address = utils.pub_2_address(self.pub_key)

        if node:
            self.init_chain()

    def new_block(self):
        """
        Mining a new block.
        """
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
        coinbase_tx = self.new_tx('0', self.address, 50, 0)
        tx_pool = self.tx_pool
        # use pop keep thread safe
        txs = [coinbase_tx] + [tx_pool.pop(0) for _ in range(len(tx_pool))]

        block = dict(header)

        # guess a nonce, this gonna takes ttttttttime
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
            # TODO del this block

    def send_coin(self, to_address, amount, fee):
        """

        :param to_address: str, receiver address
        :param amount: int,
        :param fee: int, fee paid to miner
        """
        tx = self.new_tx(self.address, to_address, amount, fee)
        tx['hash'] = utils.get_hash(tx)
        tx['signature'] = str(self.pvt_key.sign(tx['hash'].encode(), '')[0])
        tx['pub_key'] = self.pub_key
        tx['confirmation'] = 1

        # boradcast tx
        self.broadcast('tx', tx)

        return True

    def new_tx(self, from_address, to_address, amount, fee):
        """
        generate new tx

        :param from_address: str, sender address
        :param to_address: str, recevier address
        :param amount: int,
        :param fee: int, fee paid to miner
        :return: dict
        """
        tx = {
            'from': from_address,
            'to': to_address,
            'total_input': amount + fee,
            'total_output': amount,
            'ts': time.time(),
        }
        return tx

    def get_target(self):
        """
        get target hash for mining.

        :return: str
        """
        # TODO adjust target based on previous blocks' mining time
        return settings.TARGET

    def update_ledger(self, txs, ledger=None):
        """
        update ledger, from a list of txs

        :param txs: list,
        :param ledger: dict,
        :return: bool
        """
        ledger = ledger or self.ledger
        for tx in txs:
            if tx['from'] != '0':
                if ledger.get(tx['from'], 0) < tx['total_input']:
                    return False
                ledger[tx['from']] = ledger.get(tx['from']) - tx['total_input']

            ledger[tx['to']] = ledger.get(tx['to'], 0) + tx['total_output']

        return True

    def get_chain_from_node(self, node, entire_chain=True):
        """
        get entire chain from a node

        :param node: str,
        :param ledger: dict,
        """
        chain = []
        ledger = {}
        block_headers = None

        if not entire_chain:
            block_headers = {block['hash']: idx for idx, block in enumerate(self.chain)}

        ret, data = utils._get(url=f'http://{node}/get_last_block')
        if not (ret and data['ok']):
            return [], {}

        height = data.get('height', -1)
        print(height)

        while height > -1:
            ret, data = utils._get(url=f'http://{node}/get_block/{height}')
            print(ret)
            if ret and data['ok']:
                block = data.get('block', {})
                print(f'verify chain: {vf.block(block)}')
                if not vf.block(block):
                    break

                if chain and chain[0]['prev_hash'] != block['hash']:
                    break

                print(f'entire chain: {entire_chain}')
                if not entire_chain and block['hash'] in block_headers.keys():
                    idx = block_headers.get(block['hash'])
                    chain = self.chain[:idx+1] + chain
                    break

                chain.insert(0, block)
                height -= 1
            else:
                return [], {}

        # update ledger
        txs = []
        for block in chain:
            txs.extend(block['tx'])
        if not self.update_ledger(txs, ledger):
            return [], {}

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
        data = {type: data, 'port': self.port}
        for node in list(self.nodes):
            url = f'http://{node}/add_{type}'
            ret, data = utils._post(url=url, json=data)
            if not ret:
                self.nodes.remove(node)

    def add_node(self, node):
        """
        Add a node to node list

        :param node: str, like 1.1.1.1:5000
        :return: bool
        """
        if node in self.chain:
            return True

        self.broadcast('node', node)
        self.nodes.append(node)
        return True

    def add_block(self, new_block, node):
        """
        Add a block to local chain

        :param new_block: dict,
        :return: bool
        """
        if not vf.block(new_block):
            return False

        for block in list(self.chain):
            if block['hash'] == new_block['hash']:
                block['confirmation'] += 1
                return True

        if new_block['prev_hash'] == self.chain[-1]['hash']:
            self.chain.append(new_block)
            self.broadcast('block', new_block)
            return True

        return self.resolve_conflicts(node)

    def resolve_conflicts(self, node):
        url = f'http://{node}/get_last_block'
        ret, data = utils._get(url=url)
        if not ret or not data['ok']:
            return False

        if data['height'] > len(self.chain):
            chain, ledger = self.get_chain_from_node(node, entire_chain=False)
            if chain:
                self.chain = chain
                self.ledger = ledger
                return True

        return False

    def add_tx(self, new_tx):
        if not vf.tx(new_tx):
            return False

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
