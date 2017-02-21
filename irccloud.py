#!/usr/bin/python -u

from websocket import create_connection
import json
import requests
import sys
import time
import traceback
from getpass import getpass
import random
import string

try:
    # Python 2.x
    from ConfigParser import SafeConfigParser
except:
    # Python 3.x
    from configparser import SafeConfigParser

try:
    # Python 2.x
    import thread
except:
    # Python 3.x
    import _thread as thread

delay = 30

# Support input() on both Python 2.x/3.x
try:
    input = raw_input
except NameError:
    pass

class IRCCloud(object):
    def __init__(self):
        self.session = ''
        self.uri = 'https://www.irccloud.com/chat/login'
        self.uri_formauth = 'https://www.irccloud.com/chat/auth-formtoken'
        self.origin = 'https://www.irccloud.com'
        self.wss = 'wss://api.irccloud.com/websocket/' + str(random.choice(string.digits))
        self.last = 0
        self.timeout = 120
        self.config = SafeConfigParser()

    def connect(self):
        for line in self.create(self.session):
            if self.last == 0:
                # Just started..
                thread.start_new_thread(self.check, ())
            self.last = self.current_time()
            self.parseline(line)

    def reload_config(self):
        self.config = SafeConfigParser()
        self.config.read('irccloud.ini')

    def auth(self):
        try:
            # Load (or reload) configuration file
            self.reload_config()

            # Check if we have any valid configuration. If we do, load it!
            good_config = True
            if self.config.has_section("auth"):
                if self.config.has_option("auth", "email") and self.config.has_option("auth", "password"):
                    user_email    = self.config.get("auth", "email")
                    user_password = self.config.get("auth", "password")
                else:
                    good_config = False
            else:
                good_config = False

            # No valid configuration? No problem!
            if good_config:
                print("[ircc-uptime] Valid configuration loaded.")
            else:
                print("[ircc-uptime] No configuration (irccloud.ini) detected (or configuration corrupted)!")
                user_email    = input("Enter your IRCCloud email: ")
                user_password = getpass("Enter your IRCCloud password: ")

                # Commit to configuration
                if not self.config.has_section("auth"):
                    self.config.add_section("auth")
                self.config.set("auth", "email", user_email)
                self.config.set("auth", "password", user_password)

                # Attempt to save configuration
                print("[ircc-uptime] Attempting to save configuration...")
                try:
                    self.configfh = open("irccloud.ini", "w")
                    self.config.write(self.configfh)
                    self.configfh.close()
                    print("[ircc-uptime] Successfully wrote configuration!")
                    self.reload_config()
                except:
                    print(traceback.format_exc())
                    print("[ircc-uptime] Unable to save configuration.")
                    try:
                        self.configfh.close()
                    except:
                        pass

            # New form-auth API needs token to prevent CSRF attacks
            print("[ircc-uptime] Authenticating...")
            token = requests.post(self.uri_formauth, headers={'content-length': '0'}).json()['token']
            data = {'email': user_email, 'password': user_password, 'token': token}
            headers = {'x-auth-formtoken': token}
            resp = requests.post(self.uri, data=data, headers=headers)
            data = json.loads(resp.text)
            if 'session' not in data:
                print('[ERROR] Wrong email/password combination. Exiting.')
                sys.exit()
            self.session = data['session']
            print("[ircc-uptime] Ready to go!")
        except requests.exceptions.ConnectionError:
            print('[error] Failed to connect...')
            raise Exception('Failed to connect')

    def create(self, session):
        h = ["Cookie: session=%s" % session]
        self.ws = create_connection(self.wss, header=h, origin=self.origin)
        print('[irccloud] Connection created.')
        while 1:
            msg = self.ws.recv()
            if msg:
                yield json.loads(msg)

    def parseline(self, line):
        def oob_include(l):
            h = {"Cookie": "session=%s" % self.session, "Accept-Encoding": "gzip"}
            requests.get(self.origin + l["url"], headers=h).json()

        try:
            locals()[line["type"]](line)
        except KeyError:
            pass

    def diff(self, time):
        return int(int(time) - int(self.last))

    def current_time(self):
        return int(time.time())

    def check(self):
        while True:
            time.sleep(5)
            diff = self.diff(self.current_time())
            if diff > self.timeout and self.last != 0:
                print('[error] Connection timed out...')
                if hasattr(self, 'ws'):
                    self.ws.close()
                return

if __name__ == "__main__":
    print((
        '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
        '+ IRCCloud uptime script -- Copyright (c) Liam Stanley 2014-2015 +\n'
        '+  More info: https://github.com/Liamraystanley/irccloud-uptime  +\n'
        '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
    ))
    try:
        while True:
            try:
                feed = IRCCloud()
                feed.auth()
                feed.connect()
            except KeyboardInterrupt:
                sys.exit()
            except:
                print(traceback.format_exc())
                print('Disconnected. Reconnecting in %s seconds.\n' % delay)
                time.sleep(delay)
                continue
    except KeyboardInterrupt:
        sys.exit()
