from utils import *
import pickle
import random

#create socket and generate keys
sBank = createSocket(8001)
(pubkey, privatekey) = generateKeys()

#send credentials to bank
id = 'user'
cardNo = '12345'

credentials = [pubkey, id, cardNo]

pickleCredentials = pickle.dumps(credentials)
sBank.connect(('localhost', 8002))
print('Connection established to bank.')


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

#creating commit
print('Creating commit.')
commit = []
commit.append('vendor')
commit.append(certificate)
commit.append(certificateSignature)
commit.append(chain[n-1])
commit.append('2018')
commit.append(n)
commit.append(pubkey)
commit.append(bankKey)

commitSignature = signRSA(pickle.dumps(commit), privatekey)

connVendor = createSocket(8004)
connVendor.connect(('localhost', 8003))

connVendor.send(pickle.dumps([commitSignature, commit]))

products = pickle.loads(connVendor.recv(1024))
for elem in products:
	print(elem)
lastIndex = n-2
# while 1:
# 	choice = 
# connVendor.send(chain[n-2])

# time.sleep(2)
# connVendor.send(chain[n-3])