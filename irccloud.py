#!/usr/bin/python

from websocket import create_connection
import json
import requests
import sys
import time
import thread
 
 
delay = 30
 
 
class IRCCloud(object):
    def __init__(self):
        self.session = ''
        self.uri = 'https://www.irccloud.com/chat/login'
        self.uri_formauth = 'https://www.irccloud.com/chat/auth-formtoken'
        self.origin = 'https://www.irccloud.com'
        self.wss = 'wss://www.irccloud.com/?since_id=0'
        self.last = 0
        self.timeout = 120
 
    def connect(self):
        for line in self.create(self.session):
            if self.last == 0:
                # Just started..
                thread.start_new_thread(self.check, ())
            self.last = self.current_time()
            self.parseline(line)
 
    def auth(self):
        try:
            if len(sys.argv) != 3:
                fn = sys.argv[0]
                if '/' in fn:
                    fn = fn.split('/')[-1]
                if '\\' in fn:
                    fn = fn.split('\\')[-1]
                print((
                    '[ERROR] Usage:\n  $ python '
                    '%s <email> <password>' % sys.argv[0]
                ))
                sys.exit()
            # New form-auth API needs token to prevent CSRF attacks
            token = requests.post(self.uri_formauth).json()['token']
            data = {'email': sys.argv[1], 'password': sys.argv[2], 'token': token}
            headers = {'x-auth-formtoken': token}
            resp = requests.post(self.uri, data=data, headers=headers)
            data = json.loads(resp.text)
            if not 'session' in data:
                print('[ERROR] Wrong email/password combination. Exiting.')
                sys.exit()
            self.session = data['session']
        except requests.exceptions.ConnectionError:
            print('[ERROR] Failed to connect...')
            raise Exception('Failed to connect')
 
    def create(self, session):
        h = ["Cookie: session=%s" % session]
        self.ws = create_connection(self.wss, header=h, origin=self.origin)
        print('[IRCCLOUD] Connection created.')
        while 1:
            msg = self.ws.recv()
            if msg:
                yield json.loads(msg)
 
    def parseline(self, line):
        def oob_include(l):
            h = {
                "Cookie": "session=%s" % self.session,
                "Accept-Encoding": "gzip"
            }
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
                print('[ERROR] Connection timed out...')
                if hasattr(self, 'ws'):
                    self.ws.close()
                return
 
if __name__ == "__main__":
    print((
        '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
        '+ IRCCloud uptime script -- Copyright (c) Liam Stanley 2014 +\n'
        '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
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
                print('Disconnected. Reconnecting in %s seconds.\n' % delay)
                time.sleep(delay)
                continue
    except KeyboardInterrupt:
        sys.exit()
