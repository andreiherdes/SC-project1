from utils import *
import os
import pickle


products = [Product('Chair', 3),
			Product('Phone', 5),
			Product('Soda',6)]

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
newHash = connUser.recv(1024)
assert SHA2(newHash) == lastHash

lastHash = newHash
newHash = connUser.recv(1024)
assert SHA2(newHash) == lastHash

#todo: adauga citire de la tastatura pt user si lista de produse la vendor

