from turtle import up
from brownie import accounts, config, SimpleStorage, network
import os


def get_account():
    if (network.show_active() == 'development'):
        account = accounts[0]
    else:
        # account = accounts.load('freecodecamp-account')
        # account = accounts.add(os.getenv('PRIVATE_KEY'))
        account = accounts.add(config['wallets']['from_key'])
    print(account)
    return account


def deploy_simple_storage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    # Transaction
    # Call
    print(simple_storage)

    stored_value = simple_storage.retrieve0()
    print(stored_value)

    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)

    updated_stored_value = simple_storage.retrieve0()
    print(updated_stored_value)
    pass


def main():
    deploy_simple_storage()
