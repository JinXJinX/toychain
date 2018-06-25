# coding=utf-8

import utils
from Crypto.PublicKey import RSA

# sorted tx keys
tx_keys = ['confirmation', 'from', 'hash', 'pub_key', 'signature', 'to',
           'total_input', 'total_output', 'ts']
# sorted tx keys
block_keys = ['confirmation', 'hash', 'nonce', 'prev_hash', 'target', 'ts',
              'tx', 'version']


def pvt_key(inp):
    """
    Check input pvt key is a valid format toychain pvt key

    :param inp: str,
    :return: bool
    """
    pass


def chain(chain):
    """
    Check required fields, and caculate whole chain from height 1

    :param chain: list of block data
    :return: bool
    """
    pass


def tx(tx):
    """
    Check required fields, and verify account money and signature

    :param tx: dict, tx data
    :return: bool
    """
    if sorted(tx.keys()) != tx_keys:
        return False

    tx2 = {}
    for key in ['from', 'to', 'total_input', 'total_output', 'ts']:
        tx2[key] = tx[key]
    tx2_hash = utils.get_hash(tx2)

    if tx2_hash != tx['hash']:
        return False

    # TODO check the 'from' address has enough money

    if not sign(tx['pub_key'], tx['hash'], int(tx['signature'])):
        return False

    return True


def sign(pub_key, tx_hash, signature):
    """

    :param pub_key: b,
    :param msg: b,
    :param signature: int,
    :return: bool
    """
    key = RSA.importKey(pub_key.encode())
    return key.verify(tx_hash.encode(), (signature, None))


def block(block):
    """
    Check required fields, and verify hash, nonce, and target

    :param block: dict, block data
    :return: bool
    """
    if sorted(block.keys()) != block_keys:
        return False

    block2 = {}
    for key in ['version', 'ts', 'prev_hash', 'nonce', 'target']:
        block2[key] = block[key]
    block2_hash = utils.get_hash(block2)

    if block2_hash != block['hash']:
        return False

    # TODO verify 'target' is correct
    if block2_hash >= block['target']:
        return False

    return True
