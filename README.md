irccloud-uptime
===============
Simple script to keep your IRCCloud up.

Installation:
-------------

    $ sudo apt-get install python-pip
    $ pip install websocket-client requests
    $ wget https://raw.githubusercontent.com/alberthdev/irccloud-uptime/master/irccloud.py
    $ chmod +x irccloud.py

Usage:
------

The easy way:

    $ ./irccloud.py
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    + IRCCloud uptime script -- Copyright (c) Liam Stanley 2014 +
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    [ircc-uptime] No configuration (irccloud.ini) detected (or configuration corrupted)!
    Enter your IRCCloud email: myemail@emailprovider.com
    Enter your IRCCloud password: (password will be hidden as you type)
    [ircc-uptime] Attempting to save configuration...
    [ircc-uptime] Successfully wrote configuration!
    [ircc-uptime] Authenticating...
    [ircc-uptime] Ready to go!
    [irccloud] Connection created.

The hard way:

  * Create/modify irccloud.ini to look like this:

    [auth]
    email=myemail@emailprovider.com
    password=yourpasswordhere

  * Then run:

    $ ./irccloud.py
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    + IRCCloud uptime script -- Copyright (c) Liam Stanley 2014 +
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    [ircc-uptime] Valid configuration loaded.
    [ircc-uptime] Authenticating...
    [ircc-uptime] Ready to go!
    [irccloud] Connection created.

TODO
----

  * Remove deperecated thread() call and use native threading module
    instead
  * Store and locate the configuration file in the user's data folder
