from web3 import Web3

infura_url = ""
web3 = Web3(Web3.HTTPProvider(infura_url))

# We haven't published on the chain
#abi
#address 
#contract = web3.eth.contract(address = address, abi = abit)

# Array with 20 names cryptocurrency <- in Solidity? Or in Python?
# functions: 
# - randome function: number among 0-19 
# - Get the word from number contract.functions.symbol().call()
# print as many underlines as the alphabets.
