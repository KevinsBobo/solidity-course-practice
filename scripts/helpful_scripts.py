from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 2000 * 10**8


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print('Deploying Mocks...')
    if len(MockV3Aggregator) <= 1:
        MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": get_account()}
        )
        # MockV3Aggregator.deploy(
        #     DECIMALS, Web3.toWei(STARTING_PRICE, 'ether'), {
        #         "from": get_account()}
        # )
    print('Mocks Deployed!')
