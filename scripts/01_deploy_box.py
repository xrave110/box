from scripts.helpful_scripts import get_account
from brownie import (
    Contract,
    network,
    Box,
)


def main():
    account = get_account()
    print("Deploying to {}".format(network.show_active()))
    box = Box.deploy({"from": account})
    print(box.retrieve())
