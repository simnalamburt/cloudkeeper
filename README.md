cloudkeeper
===============
Don't let IRCCloud disconnect you from the network. Keep being connected!

![Tachikoma doing some IRC]

> *[Tachikoma] doing some IRC (?)*

&nbsp;

How to run
--------
### A. Using [docker]
#### 1. Make a config file first.
```bash
sudo mkdir -p /srv/cloudkeeper/

sudo tee /srv/cloudkeeper/secret.toml > /dev/null <<'EOF'
email = "my.email@example.com"
password = "Type your password in here"
EOF

sudo chmod 400 /srv/cloudkeeper/secret.toml
```

#### 2. Deploy it.
```bash
docker run -d --restart=always \
    --volume /srv/cloudkeeper:/etc/cloudkeeper:ro \
    simnalamburt/cloudkeeper
```

&nbsp;

### B. Without container
Requires Python 2.6+ or 3.3+.

#### 1. Make a config file first.
```bash
cp secret.toml.example secret.toml
vim secret.toml
chmod 400 secret.toml

# Edit the secret.toml and keep it safe!
```

#### 2. Deploy it.
```bash
# Setup virtualenv beforehand
pip install -r requirements.txt
python -m cloudkeeper
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
