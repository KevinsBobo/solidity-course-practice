from scripts.helpful_scripts import get_account, FORKED_LOCAL_ENVIRONMENTS
from brownie import interface, network, config
from web3 import Web3
from scripts.get_weth import get_weth
import time

amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        get_weth()
    # ABI
    # Address
    lending_pool = get_lending_pool()
    print(lending_pool)
    # Approve sending out ERC20 tokens
    approve_erc20(amount,
                  lending_pool.address,
                  erc20_address,
                  account)
    print("Depositing...")
    tx = lending_pool.deposit(erc20_address, amount,
                              account.address, 0, {"from": account})
    tx.wait(1)
    print("Deposited!")
    # ...how much?
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    # 0.1 ETH deposited
    # 0.0825 ETH borrowable
    print("Let's borrow!")
    # DAI in terms of ETH
    dai_eth_pirce = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"])

    amount_dai_to_borrow = (1 / dai_eth_pirce) * (borrowable_eth * 0.95)
    # borrowable_eth -> borrowable_dai * 95%
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")
    # Now we will borrow!
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account}
    )
    borrow_tx.wait(1)
    print("We borrowed some DAI!")
    time.sleep(60)
    get_borrowable_data(lending_pool, account)
    repay_all(Web3.toWei(amount_dai_to_borrow, "ether"), lending_pool, account)
    # repay_all(2**256-1, lending_pool, account)
    get_borrowable_data(lending_pool, account)
    print("You just deposited, borrowed, and repayed with Aave, Brownie, and Chainlink!")


def repay_all(amount, lending_pool, account):
    approve_erc20(
        amount,
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account}
    )
    repay_tx.wait(1)
    print("Repaid!")


def get_asset_price(dai_eth_price_feed):
    # ABI
    # Address
    dai_eth_price_feed = interface.AggregatorV3Interface(dai_eth_price_feed)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, 'ether')
    print(f"The DAI/ETH price is {converted_latest_price}")
    # 0.000327178978281725
    return float(converted_latest_price)


def get_borrowable_data(lending_pool, account):
    (
        totalCollateralETH,
        totalDebtETH,
        availableBorrowsETH,
        currentLiquidationThreshold,
        ltv,
        healthFactor
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(availableBorrowsETH, "ether")
    total_collateral_eth = Web3.fromWei(totalCollateralETH, "ether")
    total_debt_eth = Web3.fromWei(totalDebtETH, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    return(float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]['lending_pool_addresses_provider'])
    lending_pool_addresses = lending_pool_addresses_provider.getLendingPool()
    # ABI
    # Address - Check!
    lending_pool = interface.ILendingPool(lending_pool_addresses)
    return lending_pool
