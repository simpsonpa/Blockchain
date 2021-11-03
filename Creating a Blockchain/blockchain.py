# -*- coding: utf-8 -*-
"""
Created on Monday, November 2 2021

@author: Paul

This script will create a very simple blockchain.

To do:
    - look at changing the hash operation to increase complexity
    - look at changing the cryptographic problem using a different verification mechanism
    - explore other hash functions... is sha256 the end all (be all)?
"""

# Import the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a blockchain

class Blockchain:
    
    def __init__(self):
        # Define a chain in the blockchain
        self.chain = []
        # Genesis chain
        self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        block = {'index':len(self.chain) + 1,                   # with each new block, increment the chain by 1
                 'timestamp': str(datetime.datetime.now()),     # give a timestamp with the time at creation
                 'proof': proof,                                # this element will store the current proof (defined later)
                 'previous_hash': previous_hash}                # this element will store the previous hash
        self.chain.append(block)
        return block

# the get_previous_block function will return the block before the current one
    def get_previous_block(self):
        return self.chain[-1]
    
# Create a proof of work problem (challenging to solve, easy to verify)
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()     # this is the hash function, explore different ones
            if hash_operation[:4] == '0000':            # solution must have 4 leading 0's to be accepted
                check_proof = True
            else:                                       # if solution is no good, then try, try again
                new_proof += 1
        return new_proof
    
# Create a function that creates a hash for each block using the sha256 hash function
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
# the is_chain_valid function will take a chain and compare hashes to ensure that the chain is valid
    def is_chain_valid(self, chain):
        previous_block = chain[0]           # define the genesis block
        block_index = 1                     # set genesis block index to 1
        while block_index < len(chain):     # create a loop to iterate over the length of the chain
            block = chain[block_index]      # recall the block at location block_index
            if block['previous_hash'] != self.hash(previous_block):     # compare previous hash in current block with the hash of the previous block
                return block_index, False       # return false and the index of the block where things went wrong
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()     #run the hash operation on the proof and previous proof
            if hash_operation[:4] != '0000':            # solution will have 4 leading 0's (increase number of 0's to increase complexity)
                return block_index, False           # return the block index and false if an error is encountered
            previous_block = block                  # update previous block
            block_index += 1                        # increment the index for the block in the chain
        return True
            
# Part 2 - "Mining" the blockchain

# Note these operations are meant to be run locally using Postman or some other hosting service. 
# I doubt this could handle 

# Creating a Web App
app = Flask(__name__)

# Creating a Blockchain

# create an instance of our previously created blockchain
blockchain = Blockchain()
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()    # use get_previous method to recall previous block
    previous_proof = previous_block['proof']            # reference the proof of previous block to get the previous proof
    proof = blockchain.proof_of_work(previous_proof)    # proof of next block in chain
    previous_hash = blockchain.hash(previous_block)     # use the hash function on previous block to get its hash
    block = blockchain.create_block(proof, previous_hash)       # create a new block using the new proof and previous hash
    response = {'message':'Congratulations, you mined a block!',
                'index':block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash']}
    return jsonify(response), 200                   # HTTP code for OK

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,              # display the chain as of iteration x for the block chain
                'length': len(blockchain.chain)}        # display the length of the chain
    return jsonify(response), 200                   # HTTP code for OK

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message':'All good. The blockchain is valid.'}
    else:
        response
    return jsonify(response), 200


# Running the app
app.run(host = '0.0.0.0', port = 5000)