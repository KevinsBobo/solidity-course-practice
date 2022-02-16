from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv
# from solcx import install_solc
# install_solc('0.8.0')

load_dotenv()

with open('./SimpleStorage.sol', 'r', encoding='utf-8') as in_file:
    simple_storage_file = in_file.read()
    # print(simple_storage_file)

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SimpleStorage.sol": {
                "content": simple_storage_file
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.8.0"
)

# print(compiled_sol)
with open('compiled_code.json', 'w', encoding='utf-8') as out_file:
    json.dump(compiled_sol, out_file)

# get bytecode
bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage'][
    'evm'
]['bytecode']['object']

# get abi
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']


rinkeby_rpc_url = os.getenv('RINKEBY_RPC_URL')
print(rinkeby_rpc_url)
# for connecting to genache
# genache_url = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(rinkeby_rpc_url))
# Rinkeby
chain_id = 4
# Ropsten
# chain_id = 3
# my_address = '0x7A8489e8057Dba3E3E1066fb38092F829D61c02B'
private_key = os.getenv('PRIVATE_KEY')
public_key = os.getenv('PUBLIC_KEY')
print(public_key)
my_address = public_key

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a trasaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce
    }
)

# print(transaction)

signed_txn = w3.eth.account.sign_transaction(
    transaction, private_key=private_key)
# send this signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(tx_hash)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Working with the contract, you always need
# Cotract Address
# Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a rreturn value
# Transaction -> Actually make a state change
print(simple_storage.functions.retrive0().call())
# print(simple_storage.functions.store(15).call())
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print(simple_storage.functions.retrive0().call())
