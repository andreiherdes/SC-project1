from utils import *
import pickle
import sys

userAcc = 100
vendorAcc = 100
#create socket and generate keys
s = createSocket(8002)
(pubkey, privatekey) = generateKeys()

#receive user credentials
s.listen(1)
connUser, _ = s.accept()
print('Connection established to user.')

credentials = pickle.loads(connUser.recv(1024))

print('Received credentials')
userPubKey = credentials[0]
userId = credentials[1]
userCardNo = credentials[2]

#create payword certificate and send it to user
paywordCertificate = []
paywordCertificate.append('broker')
paywordCertificate.append(userId)
paywordCertificate.append(connUser.getpeername())
paywordCertificate.append(pubkey)
paywordCertificate.append(userPubKey)
paywordCertificate.append('2019')
paywordCertificate.append('serial 100$')

certificateSignature = signRSA(pickle.dumps(paywordCertificate), privatekey)

connUser.send(pickle.dumps([certificateSignature, paywordCertificate]))
print('Sent signed Payword Certificate.')

#Receive user commit from vendor
socVendor = createSocket(8005)
socVendor.listen(1)
connVendor, _ = socVendor.accept()
print('Connection established to vendor.')

vendorInfo = connVendor.recv(4096)
vendorInfo = pickle.loads(vendorInfo)

#Check commit
numHashes = vendorInfo[0]
lastHash = vendorInfo[1]
chainRoot = vendorInfo[2][3]

username = vendorInfo[2][1][1]

checkHash = lastHash
hashHistory = {username : []}

for x in range(numHashes):
	checkHash = SHA2(checkHash)
	if checkHash not in hashHistory:
		hashHistory[username].append(hashHistory)
	else:
		print('One of the sent hashes has been previously sent. Unable to accept commit')
		sys.exit()

assert checkHash == chainRoot

print('Commit verified. Transfering money.')
userAcc -= numHashes
vendorAcc += numHashes
print('User acc. balance = {}c\nVendor acc. balance = {}c'.format(userAcc, vendorAcc))