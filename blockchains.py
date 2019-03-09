import hashlib 
from time import time 
import Crypto.PublicKey.RSA as RSA 
from Crypto.Signature import pkcs1_15 
from Crypto.Hash import SHA256 

class Wallet:

    def __init__ (self):
        self.key = RSA.generate(1024) 
        self.public_key = self.key.publickey()

    def make_transaction(self, data):
        key_signer = pkcs1_15.new(self.key)
        digest = SHA256.new()
        digest.update(data)
        return Transaction(data, self.public_key, key_signer.sign(digest))

    def find_my_transactions(self, chain):
        number_of_transactions = 0
        for b in range(1, chain.number_of_blocks()):
            if chain.blocks[b].transaction.public_key == self.public_key:
                number_of_transactions += 1
        return number_of_transactions
                

class Transaction:

    def __init__ (self, data, public_key, signature):
        self.data = data
        self.public_key = public_key
        self.signature = signature

    def verify_signature(self):
        digest = SHA256.new()
        digest.update(self.data)
        try:
            pkcs1_15.new(self.public_key).verify(digest, self.signature)
            return True
        except ValueError:
            return False
        
class Block: 
    
    def __init__(self, transaction, previous_hash):           
        self.previous_hash = previous_hash 
        self.transaction = transaction 
        self.time_of_creation = time() 
        self.hash_of_self = self.hash()
 
    def hash(self): 
        contents = str(self.previous_hash) + str(self.transaction) + \
                   str(self.time_of_creation)
        return hashlib.sha256(contents.encode()).hexdigest()
        
    def is_valid(self):
        return (self.hash_of_self == self.hash()) and \
            self.transaction.verify_signature()
 
class Blockchain: 
 
    def __init__(self): 
        self.blocks = [] 
        genesis = Block("",'0') 
        self.blocks.append(genesis) 
 
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

# Check that signing a Transaction works
key = RSA.generate(1024) 
public_key = key.publickey()
key_signer = pkcs1_15.new(key)

digest = SHA256.new()
digest.update(b"Svala")

signature = key_signer.sign(digest) 

t = Transaction(b"Svala", public_key, signature)
assert t.verify_signature()

# Verifiy that tampering with the data is discovered
t.data = b"Uggla"
assert not t.verify_signature()

# Check that making Transactions inside a Wallet works
swedbank = Wallet()
naughty_business = swedbank.make_transaction(b"Bribe politician")
assert naughty_business.verify_signature()

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

magnitskij = Wallet()
immoral_stuff = Block(magnitskij.make_transaction(b"Pay prostitutes"),
                      chain.blocks[-1].hash_of_self)
chain.add_block(immoral_stuff) 
assert chain.number_of_blocks() == 3 
 
# Check that chain is valid 
assert chain.is_valid() 

dodgy_stuff = Block(swedbank.make_transaction(b"Steal money from babushkas"),
                    chain.blocks[-1].hash_of_self)

chain.add_block(dodgy_stuff)
assert chain.number_of_blocks() == 4

assert swedbank.find_my_transactions(chain) == 2
assert magnitskij.find_my_transactions(chain) == 1

# Tamper with chain 
chain.blocks[1].transaction.data = b"Totally honest stuff" 

# And check that it's no longer valid 
assert not chain.is_valid()

print ("I am completely operational and all my circuits are "
       "functioning perfectly")







