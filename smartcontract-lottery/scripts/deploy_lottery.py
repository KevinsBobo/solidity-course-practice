from scripts.helpful_scripts import (
    get_account,
    get_contract,
    fund_with_link,
    listen_for_event,
    contract_to_mock
)
from brownie import Lottery, network, config, Contract
import time


def deploy_lottery():
    account = get_account()
    if len(Lottery) <= 0:
        lottery = Lottery.deploy(
            get_contract("eth_usd_price_feed").address,
            get_contract("vrf_coordinator").address,
            get_contract("link_token").address,
            config["networks"][network.show_active()]["fee"],
            config["networks"][network.show_active()]["keyhash"],
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "verify", False)
        )
        print("Deployed lottery!")
    else:
        lottery = Lottery[-1]
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery is started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 10**8
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund the contract
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    print("Lottery ended!")
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    contract_name = "vrf_coordinator"
    contract_vrf_foofrdinator = contract_to_mock[contract_name]
    contract_address = config["networks"][network.show_active(
    )][contract_name]
    vrf_foofrdinator = Contract.from_abi(
        contract_vrf_foofrdinator._name,
        contract_address,
        contract_vrf_foofrdinator.abi
    )
    event_result = listen_for_event(vrf_foofrdinator,
                                    "RandomnessRequestFulfilled", timeout=600)
    print(event_result)
    """
    from hexbytes import HexBytes
    event_result = dict(
        {
            'args': dict(
                {
                    'requestId': b'\xc2r\xe3\xc1mK\xaf\xbeH>\xa5\x00\xb9V\xd1\x06+\xf2\x91)_~_\x8el\x11#\x8d\xa4y\xe4w',
                    'output': 20382349963496122980986253540312142339888458549513259714073745270714692363498
                }
            ),
            'event': 'RandomnessRequestFulfilled',
            'logIndex': 1,
            'transactionIndex': 3,
            'transactionHash': HexBytes('0x47eda6e70cbd28335c5d67fa602ef6d6b2c28695c606a815196d5805779a51d2'),
            'address': '0xb3dCcb4Cf7a26f6cf6B120Cf5A73875B7BBc655B',
            'blockHash': HexBytes('0x6f755a1666dc22279bcc1ba0dd4c809b67b9b6dd06a1e08f38310fcda1ccdace'),
            'blockNumber': 10176849
        }
    )
    event_result['args']['requestId'] = '0x' + event_result['args']['requestId'].hex()
    event_result['args']['output'] = hex(event_result['args']['output'])
    event_result['transactionHash'] = event_result['transactionHash'].hex()
    event_result['blockHash'] = event_result['blockHash'].hex()
    json.dumps(event_result)
        {
            "args": {
                "requestId": "0xc272e3c16d4bafbe483ea500b956d1062bf291295f7e5f8e6c11238da479e477",
                "output": "0x2d100052802985ba79373463f7e3285e6c30b5b3dddfdd9d0618a793e38164ea"
            },
            "event": "RandomnessRequestFulfilled",
            "logIndex": 1,
            "transactionIndex": 3,
            "transactionHash": "0x47eda6e70cbd28335c5d67fa602ef6d6b2c28695c606a815196d5805779a51d2",
            "address": "0xb3dCcb4Cf7a26f6cf6B120Cf5A73875B7BBc655B",
            "blockHash": "0x6f755a1666dc22279bcc1ba0dd4c809b67b9b6dd06a1e08f38310fcda1ccdace",
            "blockNumber": 10176849
        }
    """
    time.sleep(5)
    print(f"{lottery.recentWinner()} in the new winner!")
    print(f"current balance: {lottery.balance()}")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
