from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
from base64 import b64encode, b64decode

publickey_pem = open('publickey.pem', 'r').read()
pubkey = RSA.importKey(b64decode(publickey_pem))
cipher = PKCS1_v1_5.new(pubkey)

def encryt(text):
  return cipher.encrypt(text.encode())

def encryt_base64(text):
  return b64encode(encryt(text))