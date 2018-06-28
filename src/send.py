# coding=utf-8
from argparse import ArgumentParser

import toychain
import config


def tool_send_coin():
    parser = ArgumentParser()
    parser.add_argument('-to', '--address', type=str, help='send coin to this address')
    parser.add_argument('-a', '--amount', type=int, help='amount of coin')
    parser.add_argument('-f', '--fee', type=int, help='fee for miner')
    args = parser.parse_args()
    address = args.address
    amount = args.amount
    fee = args.fee

    if None in (address, amount, fee):
        return

    # lode config from config file
    tc = toychain.ToyChain(config.PORT, pvt_key=config.PVT_KEY, node=False)
    rst = tc.send_coin(address, amount, fee)


if __name__ == '__main__':
    tool_send_coin()
