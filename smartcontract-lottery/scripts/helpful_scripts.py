import time
from tracemalloc import start
from async_timeout import timeout
from brownie import MockV3Aggregator, VRFCoordinatorMock, LinkToken
from web3 import Web3
from brownie import network, config, accounts, Contract, interface, web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 2000 * 10**8


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


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken
}

DECIMALS = 8
STARTING_PRICE = 2000 * 10**8


def deploy_mocks(decimals=DECIMALS, starting_price=STARTING_PRICE):
    account = get_account()
    MockV3Aggregator.deploy(
        decimals, starting_price, {"from": account}
    )
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token, {"from": account})
    print('Mocks Deployed!')


def get_contract(contract_name):
    """This function will grab the contract address from the brownie config
    if defined, otherwise, it will deploy amock version of the contract,
    and retrun that mock contract.

        Args:
            contract_name (string)

        Returns:
            brownie.network.contract.ProjectContract: The most recently
            deployed version of the contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active(
        )][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi)
    return contract


def fund_with_link(
    contract_address, account=None, link_token=None, amount=10**17
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # tx = link_token.transfer(contract_address, amount, {"from": account})
    link_token_contract = interface.LinkTokenInterface(link_token.address)
    tx = link_token_contract.transfer(
        contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund contract!")
    return tx


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
