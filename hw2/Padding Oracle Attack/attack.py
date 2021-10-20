import requests
import time
import random
from fake_useragent import UserAgent

cipher = ["00112233445566778899aabbccddeeff",
          "f9473924bd62ba19f2dd19c309289477",
          "65786c8d4972fd132ec97a3a3e518191",
          "7652a0dc44cb493881bdd841103b8bca",
          "2d4824eef54b306f093bdc5a17dc9f46",
          "a862217ecb6b80244fdba90fbb13c72b",
          "ab3de8d9653be21d635a0f8d59712836",
          "06eb64c0fbb922afd9db007f94fb9e24",
          "a899a6c0a65b687b85f45d4840d47df4"]


attack_url = "http://140.122.185.210:8080/oracle/"


def decrypt(dkci, ci_minus_one):
    text = ""
    for i in range(16):
        temp1 = dkci[2*i:2*(i+1)]
        temp2 = ci_minus_one[2 * i:2 * (i + 1)]
        plain = int(temp1, 16) ^ int(temp2, 16)
        text += chr(plain)
    print('find:', text)
    with open('ans.txt', 'a', encoding='UTF-8') as f:
        print(text, file=f)


def main():
    for ciIndx in range(1, len(cipher)):
        dk_cipher = "0" * 32
        for idx in range(1, 17):
            get_IV = False
            for testByte in range(256):
                # repeat until send success
                not_yet = True
                sleep = 5  # if connect fail sleep
                while not_yet:
                    try:
                        # generate IV
                        newIV = ""
                        for i in range(16):
                            if i == 16-idx:
                                newIV += '{:02x}'.format(testByte)
                            elif i <= 16-idx:
                                newIV += dk_cipher[i * 2: (i + 1) * 2]
                            else:
                                hexStr = dk_cipher[2*i: 2*(i+1)]
                                x = int(hexStr, 16) ^ idx
                                newIV += '{:02x}'.format(x)

                        # send and receive
                        # generate a random user-agent and add to the header
                        user_agent = UserAgent()
                        req = requests.get(url=attack_url + newIV + cipher[ciIndx],
                                           headers={'user-agent': user_agent.random})

                        print(req.text, attack_url + newIV + cipher[ciIndx])
                        print("idx = ", idx, "newIV = ", newIV)
                        not_yet = False

                        # find
                        if req.text == "valid":
                            hexStr = newIV[32-2*idx: 32-2*(idx-1)]  # c1'
                            x = int(hexStr, 16) ^ idx  # Dk(c2) = c1' xor 01, 02, ...
                            dk_cipher = dk_cipher[:32 - idx * 2] + '{:02x}'.format(x) + dk_cipher[32 - (idx * 2) + 2:]
                            print(dk_cipher)
                            get_IV = True
                    # ignore all error
                    except:
                        # if connecnt fail at the same test add the sleep time
                        sleep += random.randint(3, 5)
                        print("Connection refused by the server(wait {}sec)".format(sleep))
                        time.sleep(sleep)
                if get_IV:
                    break
        with open('key.txt', 'a', encoding='UTF-8') as f:
            print(dk_cipher, file=f)
        # decrypt and write in to ans.txt
        decrypt(dk_cipher, cipher[ciIndx-1])


main()
