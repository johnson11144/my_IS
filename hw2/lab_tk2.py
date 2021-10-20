import random
import time
from Crypto.Cipher import AES

p = bytearray.fromhex("255044462d312e350a25d0d4c5d80a34")
C = bytearray.fromhex("d06bf9d0dab8e8ef880660d2af65aa82")
IV = bytearray.fromhex("09080706050403020100A2B2C2D2E2F2")
with open("time.txt", 'r', encoding='UTF-8') as f:
    for line in f:
        # print(bytearray.fromhex(line), "\n",IV)
        e = AES.new(bytearray.fromhex(line), AES.MODE_CBC, IV)
        if C == e.encrypt(p):
            print("key:", line)
            break
