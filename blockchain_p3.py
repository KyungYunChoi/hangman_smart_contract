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
pip install py-solc-x (Doesn't work; Use sudo dnf install solc)
"""

import warnings
warnings.simplefilter("ignore", ResourceWarning)
from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version
install_solc('0.8.28')
set_solc_version('0.8.28')

from eth_tester import EthereumTester
import random
import draw_hangman as d

#-----------------------------------Solidity source code-----------------------------------#
contract_source_code = """
// SPDX-License-Identifier: UNIDENTIFIED
pragma solidity >=0.8.2 <0.9.0;

contract Hangman {

    uint256 private missedCounter;
    bool private isWin;
    bytes1 private charInput;
    string public guessedWord;
    bytes1[] private charCorrect;
    bytes1[] private charWrong;

    function setInputChar(bytes1 ch) public {
        charInput = ch;
    }

    function setMisses() public {
        missedCounter = missedCounter + 1;
    }

    function getMisses() public view returns (uint256) {
        return missedCounter;
    }

    function setGuessedWord(string memory word) public {
        guessedWord = word;
    }

    function getGuessedWord() public view returns (string memory) {
        return guessedWord;
    }

    function getCharCorrect() public view returns (bytes1[] memory) {
        return charCorrect;
    }

    function getCharWrong() public view returns (bytes1[] memory) {
        return charWrong;
    }

    function containsChar(string memory word, bytes1 char) public pure returns (bool) {
        bytes memory wordBytes = bytes(word);

        for (uint256 i = 0; i < wordBytes.length; i++) {
            if (wordBytes[i] == char) {
                return true; 
            }
        }
        return false;
    }

    function gameGuess() public {
        bool isCorrect = containsChar(guessedWord, charInput);

        if (isCorrect) {
            charCorrect.push(charInput);
        } else {
            charWrong.push(charInput);
            setMisses();
        }
        emit GuessAttempt(charInput, isCorrect);
    }

    event GuessAttempt(bytes1 char, bool isCorrect);
}
"""

#-----------------------------------Smart Contract part-----------------------------------#
eth_tester = EthereumTester()
w3 = Web3(Web3.EthereumTesterProvider(eth_tester))
owner_account = w3.eth.accounts[0]
player_account = w3.eth.accounts[1]

balance_wei = w3.eth.get_balance(owner_account)
balance_ether = w3.from_wei(balance_wei, 'ether')
print(f"Account {owner_account} has {balance_ether} Ether.")

balance_wei = w3.eth.get_balance(player_account)
balance_ether = w3.from_wei(balance_wei, 'ether')
print(f"Account {player_account} has {balance_ether} Ether.")


compiled_sol = compile_source(contract_source_code, output_values=["abi", "bin"])
#print(compiled_sol)

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



#-----------------------------------Python part-----------------------------------#

coins = ["bitcoin", "ethereum", "solana", "dogecoin", "avalanche", "stellar",
         "chainlink", "shiba inu", "polkadot", "pudge penguins",
         "bitget token", "litecoin", "hyperliquid", "near protocol", "worldcoin",
         "internet computer", "artificial superintelligence alliance",
         "thorchain", "cosmos", "optimism"]

word = random.choice(coins)
isWin = False
misses = 0
charCorrect = []
charWrong = []

# Submit the transaction that deploys the contract
tx_hash = Hangman.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

hangman = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)

word_encoded = word.encode("utf-8")
tx_hash = hangman.functions.setGuessedWord(word_encoded.decode()).transact()
w3.eth.wait_for_transaction_receipt(tx_hash)

def gameGuess(word):

    global misses, isWin, charCorrect, charWrong

    print("_" * 50 + "\n")
    charCorrect_byts = hangman.functions.getCharCorrect().call()
    charWrong_byts = hangman.functions.getCharWrong().call()
    charCorrect = [byte.decode('utf-8') for byte in charCorrect_byts]
    charWrong = [byte.decode('utf-8') for byte in charWrong_byts]

    showCorrectAndWrongGuess(word)
    d.draw(misses,charWrong)

    charInput = askPlayerInput()
    charInput_byts = charInput.encode("utf-8")
    tx_hash = hangman.functions.setInputChar(charInput_byts).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    tx_hash = hangman.functions.gameGuess().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(w3.eth.get_balance(owner_account))
    print(w3.eth.get_balance(player_account))

    for log in tx_receipt.logs:
        event = hangman.events.GuessAttempt().process_log(log)
        print(f"Guessed Character: {event['args']['char']}, Correct: {event['args']['isCorrect']}")

    misses = hangman.functions.getMisses().call()
    isWin = checkWin(charCorrect, word)

def checkWin(correct,word):

    if all(char in correct or char == ' ' for char in word):
        print("*" * 80)
        print("Congratulations! You won!")
        print("The name of the cryptocurrency is: " + word + ".")
        print("*" * 80)
        return True
    return False

def askPlayerInput():

    validInput = False

    while validInput == False:
        charInput = input('\nEnter a single character: ')
        if charInput in charCorrect or charInput in charWrong:
            print('Please enter other char.')
        elif any(char.isupper() for char in charInput):
            print('Please enter lowercase char.')
        elif charInput.isalpha() and charInput!=' ' and len(charInput)==1:
            validInput = True
        else:
            print('Please enter only one character!')
    return charInput

def showCorrectAndWrongGuess(word):

    wordSplit = list(word)

    print('Word:')
    print(word)
    for i, char in enumerate(word):
        if char == ' ':
            print(' ', end="")
        elif char in charCorrect:
            print(char, end="")
        else:
            print('-', end="")

          

if __name__ == "__main__":

    #Hangman = w3.eth.contract(abi=contract_interface["abi"], bytecode=contract_interface[bin])
    #tx_hash = Hangman.constructor(word, 7).transact()

    print("_"*50)
    print("| Welcome to Hangman!" + " " * 28 + "|")
    print("| The target word is a name of a cryptocurrency. |")

    while misses < 7 and not isWin:
        gameGuess(word)

    if misses == 7:
        d.draw(misses, charWrong)
        print("_"*50)
        print("Game Over! You lost. :(")
        print("The word is:", word)