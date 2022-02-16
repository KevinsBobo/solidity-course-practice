import time
from brownie import (
    Lottery,
    accounts,
    config,
    network,
    exceptions,
    Contract
)
import pytest
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
    get_contract,
    contract_to_mock,
    listen_for_event
)


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter(
        {
            "from": get_account(),
            "value": lottery.getEntranceFee() + Web3.toWei(0.0001, "ether")
        }
    )
    lottery.enter(
        {
            "from": get_account(),
            "value": lottery.getEntranceFee() + Web3.toWei(0.0001, "ether")
        }
    )
    fund_with_link(lottery)
    lottery.endLottery({"from": account})

    contract_name = "vrf_coordinator"
    contract_vrf_coordinator = contract_to_mock[contract_name]
    contract_address = config["networks"][network.show_active(
    )][contract_name]
    vrf_foofrdinator = Contract.from_abi(
        contract_vrf_coordinator._name,
        contract_address,
        contract_vrf_coordinator.abi
    )
    event_result = listen_for_event(vrf_foofrdinator,
                                    "RandomnessRequestFulfilled", timeout=600)
    print(event_result)
    time.sleep(5)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
