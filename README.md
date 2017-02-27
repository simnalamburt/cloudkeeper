cloudkeeper
===============
Don't let IRCCloud disconnect you from the network. Keep being connected!

```bash
cp secret.toml.example secret.toml
vim secret.toml

# Edit the secret.toml and keep it safe!

pipenv install
pipenv run python -m cloudkeeper
```

#### How to use it without pipenv
```bash
# Setup virtualenv beforehand
pip install -r Pipfile.lock.txt
python -m cloudkeeper
```

#### Prerequisites
- Python 2.6+ or 3.3+

![Tachikoma doing some IRC]

> *[Tachikoma] doing some IRC (?)*

<br>

Deploy using containers
--------
Make a config file first.
```bash
sudo mkdir -p /srv/cloudkeeper/
sudo tee /srv/cloudkeeper/secret.toml > /dev/null <<'EOF'
email = "my.email@example.com"
password = "Type your password in here"
EOF
```

Running with [rkt]:
```
sudo systemd-run --slice=machine --unit=cloudkeeper \
    rkt run --dns=host \
    --volume volume-etc-cloudkeeper,kind=host,source=/srv/cloudkeeper,readOnly=true \
    --insecure-options=image \
    docker://quay.io/simnalamburt/cloudkeeper
```

Running with docker:
```bash
sudo docker run --detach \
    --name cloudkeeper \
    --restart always \
    --volume /srv/cloudkeeper:/etc/cloudkeeper:ro \
    simnalamburt/cloudkeeper
```

<br>

--------
*cloudkeeper* is primarily distributed under the terms of both the [MIT
license] and the [Apache License (Version 2.0)]. See [COPYRIGHT] for details.

[Tachikoma doing some IRC]: tachikoma.jpg
[Tachikoma]: https://en.wikipedia.org/wiki/Tachikoma
[rkt]: https://coreos.com/rkt
[MIT license]: LICENSE-MIT
[Apache License (Version 2.0)]: LICENSE-APACHE
[COPYRIGHT]: COPYRIGHT
