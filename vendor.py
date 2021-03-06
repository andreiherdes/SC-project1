from utils import *
import os
import pickle
import sys
products = [Product('Soda', 3),
			Product('Croissant', 5),
			Product('Sandwich',6)]

s = createSocket(8003)
(pubkey, privatekey) = generateKeys()

s.listen(1)
connUser, _ = s.accept()

print('Connection established to user.')

commitSignature, commit = pickle.loads(connUser.recv(1024))
print('Received commit. Checking signature.')
paywordCertificate = commit[1]
paywordCertificateSignature = commit[2]
chainRoot = commit[3]
userPubKey = commit[6]
bankPubKey = commit[7]

assert checkRSA(pickle.dumps(commit), commitSignature, userPubKey), "Commit signature has been tampered with"
assert checkRSA(pickle.dumps(paywordCertificate), paywordCertificateSignature, bankPubKey), "PayWord certificate signature has been tampered with"

print('Signatures confirmed.')

lastHash = chainRoot

# while 1:
# 	newHash = connUser.recv(1024)
# 	if newHash == 'Done':
# 		break
# 	assert SHA2(newHash) == lastHash
# 	lastHash = newHash

print('Sending product list to user.')
connUser.send(pickle.dumps(products))

hashHistory = [chainRoot]
hashNums = 0
while 1:
	chainCheck = pickle.loads(connUser.recv(10000))
	if chainCheck == 'done':
		break
	for elem in chainCheck:
		newHash = elem
		#check if hash has not been previously used
		if elem not in hashHistory:
			hashHistory.append(elem)
		else:
			print('One of the sent hashes has been previously sent. Unable to accept commit')
			sys.exit()
		#check hash validity
		assert SHA2(newHash) == lastHash
		lastHash = newHash
		hashNums += 1
		print('Hash {} verified'.format(hashNums+1))

print(hashNums)

socBank = createSocket(8004)
socBank.connect(('localhost', 8005))
print('Established connection to bank.')
print('Sending information to bank.')

bankCommit = [hashNums, lastHash, commit]

socBank.send(pickle.dumps(bankCommit))