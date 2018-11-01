# coding: utf-8
from __future__ import unicode_literals, absolute_import
import json
import time
import random
import string
from threading import Thread

import requests
from websocket import create_connection


#
# Constants
#
URL_LOGIN = 'https://www.irccloud.com/chat/login'
URL_FORMAUTH = 'https://www.irccloud.com/chat/auth-formtoken'
URL_ORIGIN = 'https://www.irccloud.com'
URL_WEBSOCKET = 'wss://api.irccloud.com/websocket/' + random.choice(string.digits)


def auth(user_email, user_password):
    # Retrieve a CSRF token
    resp = requests.post(URL_FORMAUTH, headers={'content-length': '0'})
    token = resp.json()['token']

    # Retrieve a session key
    data = {'email': user_email, 'password': user_password, 'token': token}
    headers = {'x-auth-formtoken': token}
    resp = requests.post(URL_LOGIN, data=data, headers=headers)
    session = json.loads(resp.text).get('session')

    # Return session
    return session


def check(context, timeout):
    while True:
        time.sleep(5)
        diff = time.time() - context['last']
        if diff <= timeout or context['last'] == 0:
            continue

        # TODO: Is it connection timeout? Why this happens?
        if context['socket'] is not None:
            context['socket'].close()
            # TODO: Shall we raise an Exception in here?
        return


def connect(session, timeout=120.0, on_succeeded=None, on_disconnect=None):
    # 여러 스레드가 동시에 접근할 정보들
    context = {
        'last': 0,
        'socket': create_connection(
            URL_WEBSOCKET,
            header=['Cookie: session={}'.format(session)],
            origin=URL_ORIGIN
        ),
    }

    if on_succeeded is not None:
        on_succeeded()

    thread = Thread(target=check, args=(context, timeout))
    thread.start()

    while True:
        payload = context['socket'].recv()
        if not payload:
            break
        context['last'] = time.time()

        msg = json.loads(payload)
        # TODO: Do something with msg

    if on_disconnect is not None:
        on_disconnect()
