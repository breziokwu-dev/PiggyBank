from web3 import Web3
import os
from dotenv import load_dotenv
import json

load_dotenv()


infura_url = os.getenv("Infura_url")
private_key = os.getenv("private_key")
web3 = Web3(Web3.HTTPProvider(infura_url))
address = web3.to_checksum_address(os.getenv("address"))


print(f"Contract address: {address}")
print(f"Connected: {web3.is_connected()}")

abi_string = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"depositor","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"deposit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalDeposited","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}] '
abi = json.loads(abi_string)

contract = web3.eth.contract(address=address, abi=abi)

def deposit_eth(amount_in_ether):
    value = web3.to_wei(amount_in_ether, 'ether')

    account = web3.eth.account.from_key(private_key)

    transaction = contract.functions.deposit().build_transaction({
        "from": account.address,
        "value": value,
        "gas": 200000,
        "gasPrice": web3.to_wei('40', 'gwei'),
        "nonce": web3.eth.get_transaction_count(account.address)
    })
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction confirmed: {tx_hash.hex()}")


def withdraw_eth(amount_in_ether):
    value = web3.to_wei(amount_in_ether, 'ether')

    account = web3.eth.account.from_key(private_key)

    transaction = contract.functions.withdraw(value).build_transaction({
        "from": account.address,
        "gas": 200000,
        "gasPrice": web3.to_wei('40', 'gwei'),
        "nonce": web3.eth.get_transaction_count(account.address)
    })
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction confirmed: {tx_hash.hex()}")

def get_balance():
    return web3.from_wei(contract.functions.getBalance().call(), 'ether')

# if __name__ == "__main__":
#     print(f"Balance before: {get_balance()} ETH")
#     deposit_eth(0.01)
#     print(f"Balance after deposit: {get_balance()} ETH")
#     withdraw_eth(0.01)
#     print(f"Balance after withdraw: {get_balance()} ETH")

print(f"Current balance: {get_balance()} ETH")