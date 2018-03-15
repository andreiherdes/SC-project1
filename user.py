from utils import *
import pickle
import random
import time

#create socket and generate keys
sBank = createSocket(8001)
(sign_pubkey, sign_privatekey) = generateKeys()

#send credentials to bank
id = 'user'
cardNo = '12345'

credentials = [sign_pubkey, id, cardNo]

pickleCredentials = pickle.dumps(credentials)
sBank.connect(('localhost', 8002))
print('Connection established to bank.')

# sBank.send(pickle.dumps(encr_pubkey))
# bank_pubkey = pickle.loads(sBank.recv(1024))
sBank.send(pickleCredentials)
print('Sent credentials to bank.')
#receive payword certificate and signature from bank
#verify signature
certificateSignature, certificate = pickle.loads(sBank.recv(1024))
bankKey = certificate[3]

print('Received Payword Certificate. Confirming certificate signature...')
assert checkRSA(pickle.dumps(certificate), certificateSignature, bankKey), "Payword certificate certificateSignature has been tampered with"
print('Signature confirmed.')

#create hash chain
print('Generating hash chain.')
n = 100
chain = []
randomSeed = str(random.random()*100)
chain.append(randomSeed)

for i in range(1, n):
	chain.append(SHA2(chain[i-1]))
print(len(chain))

chain.extend(chain)
#creating commit
print('Creating commit.')
commit = []
commit.append('vendor')
commit.append(certificate)
commit.append(certificateSignature)
commit.append(chain[n-1])
commit.append('2018')
commit.append(n)
commit.append(sign_pubkey)
commit.append(bankKey)

commitSignature = signRSA(pickle.dumps(commit), sign_privatekey)

connVendor = createSocket(8004)
connVendor.connect(('localhost', 8003))

connVendor.send(pickle.dumps([commitSignature, commit]))
print('Sent commit.')

products = pickle.loads(connVendor.recv(1024))
print('Received product list.')

for elem in products:
	print(elem)

lastIndex = n-2+100
choice = int(input('Choose product: '))

while 1:
		price = products[choice-1].price
		sendChain = chain[lastIndex:lastIndex-price:-1]
		lastIndex = lastIndex - price
		if lastIndex < 0:
			connVendor.send(pickle.dumps('done'))
			print('Out of elements in chain.')
			break
		if choice == 0:
			connVendor.send(pickle.dumps('done'))
			print('Exiting.')
			break
		connVendor.send(pickle.dumps(sendChain))
		choice = int(input('Choose product: '))
