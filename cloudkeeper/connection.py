# coding: utf-8
from __future__ import unicode_literals, absolute_import
import json
import sys
import time
import random
import string
if sys.version_info >= (3,):
    import _thread as thread
else:
    import thread

import requests
from websocket import create_connection


#
# Constants
#
URL_LOGIN = 'https://www.irccloud.com/chat/login'
URL_FORMAUTH = 'https://www.irccloud.com/chat/auth-formtoken'
URL_ORIGIN = 'https://www.irccloud.com'
URL_WEBSOCKET = 'wss://api.irccloud.com/websocket/' + random.choice(string.digits)


class IRCCloud(object):
    def __init__(self):
        self.session = ''
        self.last = 0
        self.timeout = 120

    def connect(self, on_succeeded, on_disconnect):
        enumerator = self.create(self.session)
        on_succeeded()
        for line in enumerator:
            if self.last == 0:
                # Just started..
                thread.start_new_thread(self.check, (on_disconnect,))
            self.last = self.current_time()
            self.parseline(line)
        on_disconnect()

    def auth(self, user_email, user_password):
        # Retrieve a CSRF token
        resp = requests.post(URL_FORMAUTH, headers={'content-length': '0'})
        token = resp.json()['token']

        # Retrieve a session key
        data = {'email': user_email, 'password': user_password, 'token': token}
        headers = {'x-auth-formtoken': token}
        resp = requests.post(URL_LOGIN, data=data, headers=headers)
        session = json.loads(resp.text).get('session')

        self.session = session
        return session

    def create(self, session):
        h = ['Cookie: session=%s' % session]
        self.ws = create_connection(URL_WEBSOCKET, header=h, origin=URL_ORIGIN)
        while True:
            msg = self.ws.recv()
            if not msg:
                break
            yield json.loads(msg)

    def parseline(self, line):
        # TODO: 정리
        def oob_include(l):
            h = {'Cookie': 'session={}'.format(self.session), 'Accept-Encoding': 'gzip'}
            requests.get(URL_ORIGIN + l['url'], headers=h).json()

        try:
            locals()[line['type']](line)
        except KeyError:
            pass

    def diff(self, current_time):
        return int(int(current_time) - int(self.last))

    def current_time(self):
        return int(time.time())

    def check(self, on_disconnect):
        while True:
            time.sleep(5)
            diff = self.diff(self.current_time())
            if diff > self.timeout and self.last != 0:
                # TODO: Is it connection timeout? Why this happens?
                on_disconnect()
                if hasattr(self, 'ws'):
                    self.ws.close()
                    # TODO: Shall we raise an Exception in here?
                return
