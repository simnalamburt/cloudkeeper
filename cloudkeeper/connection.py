# coding: utf-8

# Copyright 2017 Hyeon Kim
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

from __future__ import unicode_literals
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


class IRCCloud(object):
    def __init__(self):
        self.session = ''
        self.uri = 'https://www.irccloud.com/chat/login'
        self.uri_formauth = 'https://www.irccloud.com/chat/auth-formtoken'
        self.origin = 'https://www.irccloud.com'
        self.wss = 'wss://api.irccloud.com/websocket/' + random.choice(string.digits)
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
        token = requests.post(self.uri_formauth, headers={'content-length': '0'}).json()['token']

        # Retrieve a session key
        data = {'email': user_email, 'password': user_password, 'token': token}
        headers = {'x-auth-formtoken': token}
        resp = requests.post(self.uri, data=data, headers=headers)

        session = json.loads(resp.text).get('session')
        self.session = session
        return session

    def create(self, session):
        h = ['Cookie: session=%s' % session]
        self.ws = create_connection(self.wss, header=h, origin=self.origin)
        while True:
            msg = self.ws.recv()
            if not msg:
                break
            yield json.loads(msg)

    def parseline(self, line):
        def oob_include(l):
            h = {'Cookie': 'session=%s' % self.session, 'Accept-Encoding': 'gzip'}
            requests.get(self.origin + l['url'], headers=h).json()

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
                on_disconnect()
                if hasattr(self, 'ws'):
                    self.ws.close()
                    # TODO: Shall we raise an Exception in here?
                return
