import Crypto.PublicKey.RSA as RSA
import os
import hashlib

def SHA2(plaintext):
	#hash pe plaintext cu sha-2
	m = hashlib.sha256(plaintext.encode())
	return m.digest()



if __name__ == "__main__":
	pass