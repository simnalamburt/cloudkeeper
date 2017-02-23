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

> *[Tachikoma] doing some IRC*

<br>

Deploy using Docker
--------
```bash
# Make configuration
sudo mkdir -p /srv/cloudkeeper/
sudo tee /srv/cloudkeeper/secret.toml > /dev/null <<'EOF'
email = "my.email@example.com"
password = "Type your password in here"
EOF

# Run docker
sudo docker run --detach \
    --name cloudkeeper \
    --restart always \
    --volume /srv/cloudkeeper:/etc/cloudkeeper:Z \
    simnalamburt/cloudkeeper
    gitlab/gitlab-ce:latest
```

<br>

--------
*cloudkeeper* is primarily distributed under the terms of both the [MIT
license] and the [Apache License (Version 2.0)]. See [COPYRIGHT] for details.

[Tachikoma doing some IRC]: tachikoma.jpg
[Tachikoma]: https://en.wikipedia.org/wiki/Tachikoma
[MIT license]: LICENSE-MIT
[Apache License (Version 2.0)]: LICENSE-APACHE
[COPYRIGHT]: COPYRIGHT
