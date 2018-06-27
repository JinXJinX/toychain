# coding=utf-8
from argparse import ArgumentParser

import toychain


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-to', '--address', type=str, help='send coin to this address')
    parser.add_argument('-a', '--amount', type=int, help='amount of coin')
    parser.add_argument('-f', '--fee', type=int, help='fee for miner')
    args = parser.parse_args()
    address = args.address
    amount = args.amount
    fee = args.fee

    # lode config from config file
    port = "?"
    tc = toychain.ToyChain(port, pvt_key="", node=False)
