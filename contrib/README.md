Run cloudkeeper as a systemd service
--------

### A. Install
```shell
sudo cp cloudkeeper.service /etc/systemd/system/
sudo systemctl daemon-reload

sudo systemctl enable cloudkeeper
sudo systemctl start cloudkeeper
```

### B. Uninstall
```shell
sudo systemctl stop cloudkeeper
sudo systemctl disable cloudkeeper

sudo rm /etc/systemd/system/cloudkeeper.service
```

###### References
- https://coreos.com/rkt/docs/latest/using-rkt-with-systemd.html
