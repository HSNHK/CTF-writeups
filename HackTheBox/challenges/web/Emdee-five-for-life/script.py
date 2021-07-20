import requests
import hashlib
import sys
import re


def main(url):
    request = requests.session()
    body = request.get(url).text
    text = re.search("<h3 align='center'>+.*?</h3>",body)
    text = re.search(">+.*?<",text[0])
    hash = hashlib.md5(text[0][1:-1].encode()).hexdigest()
    response = request.post(url = url, data = {"hash":hash})
    flag = re.search("HTB{+.*?}",response.text)[0]
    print(flag)

if __name__=="__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please enter the challenge URL")
