import requests

cipher = ["0123456789abcdef0123456789abcdef",
          "462f0aec8f910e6b5daf6c47947de80c",
          "954a8b97fa9e58780f8298c6d06c05de",
          "0ab8b4d1a0bc03cf7c8ba306360a4f13",
          "725bc1e1021f34885a4c5349155c6ab9",
          "1c9a22110d07dbc3f150672aeeb09b95",
          "baa2f7ea8b9b04644313c7787891f588",
          "4b4366499578d84631e0a488c63d7198",
          "bde5d0f8737ce6d6964da64bc674eadf",
          "9056091bbe674d781fe835384b296622",
          "643a7bd79c6d1c7f06185a26d5c81b25",
          "873d88850b6f79ff6865dfbc5c9a0e8e",
          "c000bf26daf8fe54a801fc11e0e68fed",
          "700c7bfef81206d028dfbef3d0311cb1"]


attack_url = "http://140.122.185.173:8080/oracle/"

# cipher[0] 4c5a6517e6dca89d21452912fbd9a48a

def decrypt(dkci, ci_minus_one):
    text = ""
    for i in range(16):
        temp1 = dkci[2*i:2*(i+1)]
        temp2 = ci_minus_one[2 * i:2 * (i + 1)]
        plain = int(temp1, 16) ^ int(temp2, 16)
        text += chr(plain)
    print(text)
    return text


plainTextList = []

for ciIndx in range(1, 14):

    dk_cipher = "0" * 32
    for idx in range(1, 17):

        for testByte in range(256):

            newIV = ""
            for i in range(16):
                if (i == 16-idx):
                    newIV += '{:02x}'.format(testByte)
                elif (i <=16 - (idx)):
                    newIV += dk_cipher[i * 2: (i + 1) * 2]
                else:
                    hexStr = dk_cipher[2*(i): 2*(i+1)]
                    x = int(hexStr, 16) ^ idx
                    newIV += '{:02x}'.format(x)


            req = requests.get(attack_url + newIV + cipher[ciIndx])

            print(req.text)
            print("idx = ", idx, "newIV = ", newIV)

            if (req.text == "valid"):
                hexStr = newIV[32-2*(idx): 32-2*(idx-1)] # c1'
                x = int(hexStr, 16) ^ idx # Dk(c2) = c1' xor 01, 02, ...
                dk_cipher = dk_cipher[:32 - ((idx) * 2)] + '{:02x}'.format(x) + dk_cipher[32 - ((idx) * 2) + 2:]
                print(dk_cipher)
                break

    plain = decrypt(dk_cipher, cipher[ciIndx-1])
    plainTextList.append(plain)

for i in plainTextList:
    print(i)