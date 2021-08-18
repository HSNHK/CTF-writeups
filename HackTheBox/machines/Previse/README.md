# Previse

The first thing we're going to do is run the Nmap scan 
```
nmap -sC -sV [IP]
```
<p align="center">
<img src="./images/Scan.JPG">
</p>

As a result of this Nmap scan, I discovered a port `22 SSH` and 80

<p align="center">
<img src="./images/Login.JPG">
</p>

Next, I used `gobuster` to brute force the directory.

```bash
gobuster dir -u http://10.10.11.104 -w ./directory-list-2.3-medium.txt -x php
```

A list of routes can be found in the image below:

<p align="center">
<img src="./images/Directory-brute-force.JPG">
</p>

Furthermore, I have discovered an interesting directory which is `nav.php`, while analyzing this report.

Therefore, I found that it is possible to `create an account` in this directory.

<p align="center">
<img src="./images/nav.JPG">
</p>

This website allows the creation of accounts but this page has been redirected to `login.php`

So I created an account using tricks, and I'll explain to you how I did it.

To begin, I have opened the `burpsuite` tool to capture the request.

I have captured the request

next right-click the mouse you get the `do intercept` option and click the response to this request

<p align="center">
<img src="./images/burp.JPG">
</p>

And the send `request to response`

You now get a response in the burpsuit and change the status code from `302` to `200 Ok`. 

This trick will change `302` to `200` in the request and send the response to the browser 

<p align="center">
<img src="./images/Change_Status.JPG">
</p>

Now you can see that we can `create an account` on the website.

Create a username and password according to your wishes.

<p align="center">
<img src="./images/Account.JPG">
</p>

Next, we going to login into the website using a `username` and `password`

<p align="center">
<img src="./images/Login.JPG">
</p>

> Now we are successfully login into the site 

Next, we clicked on the `file menu`, where we found `sitebackup.zip`, which is interesting.

<p align="center">
<img src="./images/Files.JPG">
</p>

So download the file and extract it.

We got some interesting `PHP` files.

Further analyzing this I got two interesting files which are `config.php` and logs.php.

```php
<?php

function connectDB(){
    $host = 'localhost';
    $user = 'root';
    $passwd = 'mySQL_p@ssw0rd!:)';
    $db = 'previse';
    $mycon = new mysqli($host, $user, $passwd, $db);
    return $mycon;
}

?>
```
We get the username and password for the MySQL database in `config.php`.

Next to another file is `logs.php` in this file I got the one vulnerability which is `os command injection`.

```php
$output = exec("/usr/bin/python /opt/scripts/log_process.py {$_POST['delim']}");
echo $output;

$filepath = "/var/www/out.log";
$filename = "out.log";    
```

The file contains a delimiter and has not been sanitized properly, which allows us to execute `os command injections`.

So first go to that website and click the `management menu` and there is a `file log`.

Enter to file log you can able to see the delimiter. so capture this request in a burpsuit.

<p align="center">
<img src="./images/LogFile.JPG">
</p>

Before that start the netcat
```
nc -nlvp 1234
```
So injected the downloaded payload in the delimiter which is shown in the image.

<p align="center">
<img src="./images/revshell.png">
</p>

Now you get the shell in the `netcat`.

upgrade shell : 
```
python -c 'import pty; pty.spawn("/bin/sh")'
```
or
```
echo os.system('/bin/bash')
```
Next, we going to search username and password in the `MySQL` database 

We got one interesting file in the site backup folder which is `config.php`

In this file, there is a username and password, and a database also.
```
mysql -u root -D previse -p
```
Now it will ask the password so enter the password `mySQL_p@ssw0rd!:)`

Now you can able to enter it into in MySQL database.
<p align="center">
<img src="./images/selectaccount.png">
</p>
Yes the hash password of the user we just found. I decoded the hash code. I’ll post it here as an exception for friends with weak machines. 

`$1$🧂llol$DQpmdvnb7EeuO6UaqRItf.` = `ilovecody112235!` 

Now that we have found our user information, let’s connect with the ssh port.
```
ssh m4lwhere@10.10.11.104
```
<p align="center">
<img src="./images/userflag.JPG">
</p>
