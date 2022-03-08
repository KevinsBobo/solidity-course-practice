import time
from brownie import network, config, accounts, web3
import eth_utils

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def listen_for_event(brownie_contract, event, timeout=200, poll_interval=2):
    """Listen for an event to be fired from a contract.
    We are waiting for the event to return, so this function is blocking.

    Args:
        brownie_contract ([brownie.network.contract.ProjectContract]):
        A brownie contract of some kind.

        event ([string]): The event you'd like to listen for.

        timeout (int, optional): The max amount in seconds you'd like to
        wait for that event to fire. Defaults to 200 seconds.

        poll_interval ([int]): How often to call your node to check for events.
        Defaults to 2 seconds.
    """
    web3_contract = web3.eth.contract(
        address=brownie_contract.address, abi=brownie_contract.abi
    )
    start_time = time.time()
    current_time = time.time()
    event_filter = web3_contract.events[event].createFilter(fromBlock="latest")
    while current_time - start_time < timeout:
        for event_response in event_filter.get_new_entries():
            if event in event_response.event:
                print("Found event!")
                return event_response
        time.sleep(poll_interval)
        current_time = time.time()
    print("Timeout reached, no event found")
    return {"event": None}


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")

    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_function_call,
                {"from": account}
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address,
                new_implementation_address,
                {"from": account}  # , "gas_limit": 10**6}
            )
    elif initializer:
        encoded_function_call = encode_function_data(initializer, *args)
        transaction = proxy.upgradeToAndCall(
            new_implementation_address,
            encoded_function_call,
            {"from": account}
        )
    else:
        transaction = proxy.upgradeTo(
            new_implementation_address,
            {"from": account}  # , "gas_limit": 10**6, "allow_revert": True}
        )
    if transaction:
        transaction.wait(1)
    return transaction
