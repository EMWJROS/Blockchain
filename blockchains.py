import hashlib 
from time import time
import Crypto.PublicKey.RSA as RSA

class Wallet:

    def __init__ (self):
        self.key = RSA.generate(1024) 
        self.public_key = self.key.publickey()

    def make_transaction(self, receiver, amount):
        return Transaction(self.public_key, receiver, amount)

    def find_my_transactions(self, chain):
        number_of_transactions = 0
        for b in range(1, chain.number_of_blocks()):
            if chain.blocks[b].transaction.sender == self.public_key:
                number_of_transactions += 1
        return number_of_transactions

class Transaction:

    sequence_number = 0

    def __init__ (self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.sequence_number = Transaction.sequence_number
        self.transaction_id = hashlib.sha256(self.data().encode()).hexdigest()
        Transaction.sequence_number += 1

    def data(self):
        return str(self.sender) + str(self.receiver) + str(self.amount) + \
                  str(self.sequence_number)

    def verify(self):
        return self.transaction_id == hashlib.sha256(
            self.data().encode()).hexdigest()

class Block: 
    
    def __init__(self, transactions, bank, miner):           
        self.time_of_creation = time()
        self.data = transactions
        self.data.append(Transaction(bank, miner, 1.0))
        self.nonce = 0
        self.hash_of_self = ""
 
    def hash(self): 
        contents = str(self.previous_hash) + str(self.data) + \
                   str(self.time_of_creation) + str(nonce)
        return hashlib.sha256(contents.encode()).hexdigest()
        
    def is_valid(self):
        return (self.hash_of_self == self.hash())
            # self.transaction.verify()

    def proof_of_work(self):
        return self.hash()[1:] == "0"

    def mine(self):
        while not self.proof_of_work():
            nonce += 1
        self.hash_of_self = self.hash()
 
class Blockchain: 
 
    def __init__(self): 
        self.blocks = [] 
        self.transactions = [] 
        genesis = Block("",'0') 
        self.blocks.append(genesis)
        self.wallet = Wallet()

    def add_new_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions

    def get_block_template(self, miner):
        return Block(self.transactions, self.wallet.public_key, miner)
 
    def number_of_blocks(self): 
        return len(self.blocks)

    def add_block(self, block):
        if block.is_valid():
            block.previous_hash = self.blocks[-1].hash()
            self.blocks.append(block)
 
    def is_valid(self): 
        status = True 
        num_blocks = self.number_of_blocks() 
        for b in range(1, num_blocks): 
            status = status and (self.blocks[b-1].hash() == 
                                  self.blocks[b].previous_hash) and \
                                  self.blocks[b].is_valid()
        return status and self.blocks[-1].is_valid()


# Check that making Transactions inside a Wallet works
swedbank = Wallet()
naughty_business = swedbank.make_transaction(b"Politician", 1000000)
assert naughty_business.verify()

# Check that genesis works 
chain = Blockchain() 
assert chain.number_of_blocks() == 1 

# Create a block from a transaction
new_block = Block(naughty_business, chain.blocks[-1].hash_of_self)

assert new_block.is_valid()

# Check that we can add blocks to chain
chain.add_block(new_block) 
assert chain.number_of_blocks() == 2 
 
# Check that chain is valid 
assert chain.is_valid() 

oligarch = Wallet()
immoral_stuff = Block(oligarch.make_transaction(b"Prostitute", 5000),
                      chain.blocks[-1].hash_of_self)
chain.add_block(immoral_stuff) 
assert chain.number_of_blocks() == 3 
 
# Check that chain is valid 
assert chain.is_valid() 

dodgy_stuff = Block(swedbank.make_transaction(b"Babushka",
                                              -10000),
                    chain.blocks[-1].hash_of_self)

chain.add_block(dodgy_stuff)
assert chain.number_of_blocks() == 4

assert swedbank.find_my_transactions(chain) == 2
assert oligarch.find_my_transactions(chain) == 1

# Tamper with chain 
chain.blocks[1].transaction.receiver = b"The Pope" 

# And check that it's no longer valid 
assert not chain.is_valid()

print ("I am completely operational and all my circuits are "
       "functioning perfectly")







