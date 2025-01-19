# -*- coding: utf-8 -*-
"""blockchain_p3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ptUY3-Zag7v4NWtyq-4s1J_mWSDKznRI
"""
"""
Requirements:
pip install web3==6.0.0b11
pip install -U "web3[tester]"
pip install py-solc-x
"""

from solcx import get_installable_solc_versions
#print(get_installable_solc_versions())

from web3 import Web3
from solcx import install_solc, set_solc_version
install_solc('0.8.28') # Install a specific solc version.
set_solc_version('0.8.28') # Set Solidity version for compilation
from solcx import compile_source
import random
import warnings
warnings.simplefilter("ignore", ResourceWarning)

# Solidity source code
compiled_sol = compile_source(
    '''
    pragma solidity >0.5.0;

    contract Hangman {
        string public playerName;  // Do we need?
        bool public gameRunning;
        string public word;
        string public quiz;

        constructor() public {
            playerName = '';  //do we need this?
            gameRunning = true;
        }

        function setPlayerName(string memory _playerName) public{
            playerName = _playerName;
        }

        function viewPlayerName() view public returns (string memory) {
            return playerName;
        }

        function setWord(string memory _word) public {
            word = _word;
        }

        function getWord() view public returns (string memory) {
            return word;
        }

        function setQuiz(string memory _quiz) public {
            quiz = _quiz;
        }

        function getQuiz() view public returns (string memory) {
            return quiz;
        }
    }
    ''',
    output_values=['abi', 'bin']
)

# retrieve the contract interface
contract_id, contract_interface = compiled_sol.popitem()

# get bytecode / bin
bytecode = contract_interface['bin']

# get abi
abi = contract_interface['abi']

# web3.py instance
w3 = Web3(Web3.EthereumTesterProvider())

# set pre-funded account as sender
w3.eth.default_account = w3.eth.accounts[0]

Hangman = w3.eth.contract(abi=abi, bytecode=bytecode)

# Submit the transaction that deploys the contract
tx_hash = Hangman.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

hangman = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)

# Word bag
coins = ["bitcoin", "ethereum", "solana", "dogecoin", "avalanche", "stellar", "chainlink", "shiba inu", "polkadot", "pudge penguins",
         "bitget token", "litecoin", "hyperliquid", "near protocol", "worldcoin", "internet computer", "artificial superintelligence alliance", "thorchain", "cosmos", "optimism",]


# choose a word randomly
word = random.choice(coins)

# send to contract
tx_hash = hangman.functions.setWord(word).transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Show alphabet with '_' and empty space with "-"
def transform_string(s):
    return ''.join('_ ' if char.isalpha() else '- ' for char in s)
    
quiz = transform_string(word)
print(quiz)  # "hi hi" -> "_ _ - _ _ "

# send to the contract
tx_hash = hangman.functions.setQuiz(quiz).transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
