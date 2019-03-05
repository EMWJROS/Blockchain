import hashlib
from time import time

class Block:

    def __init__(self, data, previous_hash):
        
        self.previous_hash = previous_hash
        self.data = data
        self.time_of_creation = time()
        self.hash_of_self = self.hash()

    def hash(self):
        contents = self.previous_hash + self.data + str(self.time_of_creation)
        return hashlib.sha256(contents.encode()).hexdigest()
        

class Blockchain:

    def __init__(self):
        self.blocks = []
        genesis = Block("",'0')
        self.blocks.append(genesis)

    def number_of_blocks(self):
        return len(self.blocks)

    def add_new_block(self, data):
        new_block = Block(data, self.blocks[-1].hash_of_self)
        self.blocks.append(new_block)

    def is_valid(self):
        status = True
        num_blocks = self.number_of_blocks()
        for b in range(1, num_blocks):
            status = status and (self.blocks[b-1].hash() ==
                                 self.blocks[b].previous_hash)
        return status

# Check that previos hash is ok        
new_block = Block("apa", '1')
assert new_block.previous_hash == '1'

# Check that time of creation differs
another_block = Block("apa", '1')
assert new_block.time_of_creation != another_block.time_of_creation

# Check that linking of blocks works
linked_block = Block("bepa", new_block.hash_of_self)
assert linked_block.previous_hash == new_block.hash_of_self

# Check that genesis works
chain = Blockchain()
assert chain.number_of_blocks() == 1

# Check that we can add blocks
chain.add_new_block("cykel")
assert chain.number_of_blocks() == 2

# Check that chain is valid
assert chain.is_valid()

chain.add_new_block("u-båt")
assert chain.number_of_blocks() == 3

# Check that chain is valid
assert chain.is_valid()

# Tamper with chain
chain.blocks[1].data = "kärnkraftverk"

# And check that it's no longer valid
assert not chain.is_valid()