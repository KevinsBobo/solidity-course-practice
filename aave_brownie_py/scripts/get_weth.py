from scripts.helpful_scripts import get_account
from brownie import interface, network, config
from web3 import Web3


def main():
    get_weth()


def get_weth():
    """
    Mints WETH  by depositing ETH.
    """
    # ABI
    # Address
    account = get_account()
    weth = interface.WethInterface(
        config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": Web3.toWei(0.1, "ether")})
    tx.wait(1)
    print("Received 0.1 WETH")
    return tx
