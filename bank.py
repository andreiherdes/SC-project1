from utils import *
import pickle

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