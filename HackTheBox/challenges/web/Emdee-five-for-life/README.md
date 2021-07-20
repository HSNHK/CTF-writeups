# Emdee five for life writeup
<b>Starting point</b>

our only task is to submit the string after converting it to md5 hash 

but when i tried to submit i got this
> Yup Too slow

We'll automate this by writing a Python script

# page source
```html
<html>
<head>
<title>emdee five for life</title>
</head>
<body style="background-color:powderblue;">
<h1 align='center'>MD5 encrypt this string</h1><h3 align='center'>B6KsLl2q3nMwLszk3DVJ</h3><center><form action="" method="post">
<input type="text" name="hash" placeholder="MD5" align='center'></input>
</br>
<input type="submit" value="Submit"></input>
</form></center>
</body>
</html>
```

# Building the script
So with my crappy skills of regex let’s start building the logic

`><h3 align='center'>sR1LvFdED1Toos1uBn6k</h3>`

This was achieved by using this

`center'>+.*?</h3>`

# script
```python
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

```
# Getting the flag
```
D:\hackthebox\web>python script.py http://46.101.20.243:30585/
HTB{*-*-*-*-*-*-*-*-*-*}
```

