from  utils import *


plaintext = 'keklord'
key = RSA.generate(1024, os.urandom)

signature = key.sign(plaintext.encode(), '')
pubkey = key.publickey()

assert pubkey.verify(plaintext, signature)