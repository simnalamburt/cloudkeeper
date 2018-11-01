cloudkeeper
===============
Don't let IRCCloud disconnect you from the network. Keep being connected!

![Tachikoma doing some IRC]

> *[Tachikoma] doing some IRC (?)*

&nbsp;

How to run
--------
### A. With [docker]
```bash
docker run -d --restart=always \
  -e CLOUDKEEPER_EMAIL=user@example.com \
  -e CLOUDKEEPER_PASSWORD=yoursecretpassword \
  simnalamburt/cloudkeeper
```

&nbsp;

### B. Without [docker]
Requires Python 2.6+ or 3.3+.
```bash
# Setup virtualenv first

pip install --editable .

export CLOUDKEEPER_EMAIL=user@example.com
export CLOUDKEEPER_PASSWORD=yoursecretpassword
python -m cloudkeeper
```

Testing
```bash
pip install flake8
flake8
```

Packaging
```bash
pip install wheel
python setup.py sdist bdist_wheel
```


&nbsp;

--------
*cloudkeeper* is primarily distributed under the terms of both the [MIT
license] and the [Apache License (Version 2.0)]. See [COPYRIGHT] for details.

[Tachikoma doing some IRC]: tachikoma.jpg
[Tachikoma]: https://en.wikipedia.org/wiki/Tachikoma
[docker]: https://docker.com/
[MIT license]: LICENSE-MIT
[Apache License (Version 2.0)]: LICENSE-APACHE
[COPYRIGHT]: COPYRIGHT
