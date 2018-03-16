from utils import *
import pickle
import sys

userAcc = 100
vendorAcc = 100
print('User acc. balance = {}'.format(userAcc))
print('Vendor acc. balance = {}'.format(vendorAcc))
#create socket and generate keys
s = createSocket(8002)
(sign_pubkey, sign_privatekey) = generateKeys()

#receive user credentials
s.listen(1)
connUser, _ = s.accept()
print('Connection established to user.')
# user_pubkey = pickle.loads(connUser.recv(1024))
# connUser.send(pickle.dumps(encr_pubkey))
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
paywordCertificate.append(sign_pubkey)
paywordCertificate.append(userPubKey)
paywordCertificate.append('2019')
paywordCertificate.append('serial 100$')

certificateSignature = signRSA(pickle.dumps(paywordCertificate), sign_privatekey)

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

for x in range(numHashes):
	checkHash = SHA2(checkHash)


assert checkHash == chainRoot, 'Did not reach chain root. Money not transferred'

print('Commit verified. Transfering money.')
userAcc -= numHashes
vendorAcc += numHashes
print('User acc. balance = {}c\nVendor acc. balance = {}c'.format(userAcc, vendorAcc))