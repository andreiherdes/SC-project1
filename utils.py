from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Hash import SHA256 
from base64 import b64encode, b64decode 

import os
import socket

def SHA2(plaintext):
	#return hash applied to plaintext
	if type(plaintext) is str:
		hash = SHA256.new(plaintext.encode()).digest()
	else:
		hash = SHA256.new(plaintext).digest()
	return hash

def signRSA(data, privatekey):
	if type(data) is str:
		hash = SHA256.new(data.encode()).digest()
	else:
		hash = SHA256.new(data).digest()
	signature = privatekey.sign(hash, '')
	return signature

def checkRSA(data, signature, pubkey):
	if type(data) is str:
		hash = SHA256.new(data.encode()).digest()
	else:
		hash = SHA256.new(data).digest()
	return pubkey.verify(hash, signature)

def generateKeys():
	'''generate public and private rsa keys'''
	keys = RSA.generate(1024, os.urandom)
	privatekey = keys
	pubkey = keys.publickey()
	return (pubkey, privatekey)

def createSocket(port, host="localhost"):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port))
	return s

def receiveMsg(s, length):
	s.listen(1)
	connection, address = s.accept()
	data = connection.recv(length).decode("UTF-8")
	return data

def sendMsg(s, port, msg, host="localhost"):
	s.connect((host, port))
	s.send(msg.encode("UTF-8"))

class Product:
	def __init__(self, name, price):
		self.name = name
		self.price = price
	def __str__(self):
		return "Name: " + name + ", " + "Price: " + price



if __name__ == "__main__":
	m = 'salut!'
	(pubkey, privatekey) = generateKeys()
	signature = signRSA(m, privatekey)
	assert checkRSA(m, signature, pubkey)