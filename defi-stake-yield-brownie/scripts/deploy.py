import json
import os
import shutil
from scripts.helpful_scripts import get_account, get_contract, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import config, network
from brownie import DappToken, TokenFarm
from web3 import Web3
from brownie.network import priority_fee
import yaml


KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_token_fram_and_dapp_token(front_end_update=False):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # priority_fee("2 gwei")
        priority_fee("auto")
    account = get_account()
    dapp_token = DappToken.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify", False
        )
    )

    token_farm = TokenFarm.deploy(
        dapp_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify", False
        )
    )

    tx = dapp_token.transfer(
        token_farm.address,
        dapp_token.totalSupply() - KEPT_BALANCE,
        {"from": account}
    )
    tx.wait(1)

    # dapp_token, weth_token, fau_token
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    dai_token = get_contract("dai_token")
    link_token = get_contract("link_token")
    dict_of_allowed_tokens = {
        dapp_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        dai_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
        link_token: get_contract("link_usd_price_feed"),
    }
    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)

    if front_end_update:
        update_front_end()
    return token_farm, dapp_token


def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = token_farm.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)
        set_tx = token_farm.setPriceFeedContract(
            token.address, dict_of_allowed_tokens[token], {"from": account}
        )
        set_tx.wait(1)
    return token_farm


def update_front_end():
    # Send the buld folder
    copy_folders_to_front_end('./build', './front_end/src/chain-info')
    # Sending the front end out config in JSON format
    with open("brownie-config.yaml", 'r', encoding='utf-8') as brrownie_config:
        config_dict = yaml.load(brrownie_config, Loader=yaml.FullLoader)
        with open('./front_end/src/brownie-config.json', 'w', encoding='utf-8') as brownie_config_json:
            json.dump(config_dict, brownie_config_json)
        print('Front end updated!')


def copy_folders_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def main():
    deploy_token_fram_and_dapp_token(front_end_update=True)
