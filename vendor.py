from utils import *
import os
import pickle

s = createSocket(8003)
(pubkey, privatekey) = generateKeys()

s.listen(1)
connUser, _ = s.accept()

print('Connection established to user.')

commitSignature, commit = pickle.loads(connUser.recv(1024))
print('Received commit. Checking signature.')
paywordCertificate = commit[1]
paywordCertificateSignature = commit[2]
userPubKey = commit[6]
bankPubKey = commit[7]
chainRoot = commit[3]

assert checkRSA(pickle.dumps(commit), commitSignature, userPubKey)
assert checkRSA(pickle.dumps(paywordCertificate), paywordCertificateSignature, bankPubKey)

lastHash = chainRoot

# while 1:
# 	newHash = connUser.recv(1024)
# 	if newHash == 'Done':
# 		break
# 	assert SHA2(newHash) == lastHash
# 	lastHash = newHash


newHash = connUser.recv(1024)
assert SHA2(newHash) == lastHash

lastHash = newHash
newHash = connUser.recv(1024)
assert SHA2(newHash) == lastHash