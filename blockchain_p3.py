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
from solcx import compile_source, install_solc
install_solc('0.8.28')

from eth_tester import EthereumTester
import random
import draw_hangman as d




#-----------------------------------Solidity source code-----------------------------------#
contract_source_code = """
pragma solidity ^0.8.0;

contract Hangman {
    string private word;
    bytes32 private hashedWord;
    address public owner;
    uint8 public maxMisses;
    uint8 public misses;
    string public guessedWord;
    bool public isGameOver;
    mapping(uint256 => bool) public guessedIndices;

    event Guess(address indexed player, string guessedWord, bool isCorrect);
    event GameOver(string result, string finalWord);

    constructor(string memory _word, uint8 _maxMisses) {
        owner = msg.sender;
        word = _word;
        hashedWord = keccak256(abi.encodePacked(_word));
        maxMisses = _maxMisses;
        misses = 0;
       // guessedWord = string(abi.encodePacked(new bytes(_word.length)));
        isGameOver = false;
    }

    function guessLetter(string memory letter) public {
        require(!isGameOver, "Game is already over.");
        require(bytes(letter).length == 1, "Guess must be a single character.");

        bytes memory wordBytes = bytes(word);
        bytes memory guessedBytes = bytes(guessedWord);
        bool isCorrect = false;

        for (uint256 i = 0; i < wordBytes.length; i++) {
            if (
                !guessedIndices[i] &&
                keccak256(abi.encodePacked(letter)) == keccak256(abi.encodePacked(wordBytes[i]))
            ) {
                guessedBytes[i] = bytes(letter)[0];
                guessedIndices[i] = true;
                isCorrect = true;
            }
        }

        guessedWord = string(guessedBytes);

        if (isCorrect) {
            emit Guess(msg.sender, guessedWord, true);
        } else {
            misses++;
            emit Guess(msg.sender, guessedWord, false);
        }

        if (misses >= maxMisses) {
            isGameOver = true;
            emit GameOver("You lost!", word);
        } else if (keccak256(abi.encodePacked(guessedWord)) == hashedWord) {
            isGameOver = true;
            emit GameOver("You won!", word);
        }
    }

    function getGuessedWord() public view returns (string memory) {
        return guessedWord;
    }
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

def gameGuess(word):

    global misses, isWin

    print("_" * 50 + "\n")
    #print('test',word)
    showCorrectAndWrongGuess(word)
    d.draw(misses,charWrong)
    charInput = askPlayerInput()

    if charInput in word:
        charCorrect.append(charInput)
        print(charInput)
    else:
        charWrong.append(charInput)
        misses+=1
        
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