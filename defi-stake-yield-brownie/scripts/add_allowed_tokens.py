from scripts.helpful_scripts import get_account, get_contract, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import network
from brownie.network import priority_fee
from brownie import DappToken, TokenFarm


def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        print(token)
        add_tx = token_farm.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)
        set_tx = token_farm.setPriceFeedContract(
            token.address, dict_of_allowed_tokens[token], {"from": account}
        )
        set_tx.wait(1)
    return token_farm


def main():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # priority_fee("2 gwei")
        priority_fee("auto")
    else:
        print("Please switch to blockchain environments!")
        return
    account = get_account()
    dapp_token = DappToken[-1]
    token_farm = TokenFarm[-1]
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
