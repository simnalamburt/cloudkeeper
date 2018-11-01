# coding: utf-8
from __future__ import unicode_literals, absolute_import
import json
import time
import random
import string
import logging
from threading import Thread

import requests
from websocket import create_connection


#
# Constants
#
URL_LOGIN = 'https://www.irccloud.com/chat/login'
URL_FORMAUTH = 'https://www.irccloud.com/chat/auth-formtoken'
URL_ORIGIN = 'https://www.irccloud.com'

logger = logging.getLogger(__name__)


def auth(email, password):
    logger.info('Starting authentication')

    # Retrieve a CSRF token
    resp = requests.post(URL_FORMAUTH, headers={'content-length': '0'})
    msg = resp.json()
    if msg.get('success') is not True or 'token' not in msg:
        return None
    token = msg['token']

    # Retrieve a session key
    data = {'email': email, 'password': password, 'token': token}
    headers = {'x-auth-formtoken': token}
    resp = requests.post(URL_LOGIN, data=data, headers=headers)
    msg = resp.json()
    if msg.get('success') is not True or 'session' not in msg:
        return None
    session = msg['session']

    logger.info('Authentication completed: {}'.format(session))
    url = 'wss://{}{}?exclude_archives=1'.format(
        msg.get('websocket_host', 'api.irccloud.com'),
        msg.get('websocket_path', '/websocket/{}'.format(random.choice(string.digits))),
    )
    return session, url


def check(context, timeout, check_period):
    while time.time() - context['last'] <= timeout:
        time.sleep(check_period)

    # TODO: Investigate when and why this happens
    logger.debug(
        ('No message on the socket for {} seconds. ' +
         'Disconnecting the socket').format(timeout)
    )
    if context['socket'] is not None:
        context['socket'].close()


def connect(session, websocket_url, timeout=120.0, check_period=5.0):
    socket = create_connection(
        websocket_url,
        header=['Cookie: session={}'.format(session)],
        origin=URL_ORIGIN,
    )
    logger.info('Connection created at {}'.format(websocket_url))

    # Send authentication message
    socket.send(json.dumps({
        'cookie': session,
        '_reqid': 1,
        '_method': 'auth',
    }))

    # 여러 스레드가 동시에 접근할 정보들
    context = {
        'last': time.time(),
        'socket': socket,
    }
    thread = Thread(target=check, args=(context, timeout, check_period), daemon=True)
    thread.start()

    while True:
        payload = context['socket'].recv()
        if not payload:
            break
        context['last'] = time.time()

        msg = json.loads(payload)
        logger.debug(msg)

        if msg.get('type') == 'oob_include':
            url = msg['url']
            headers = {
                'Cookie': 'session={}'.format(session),
                'Accept-Encoding': 'gzip',
            }
            resp = requests.get(URL_ORIGIN + url, headers=headers)
            logger.debug('Backlog retrieved, status code: {}'.format(resp.status_code))

    logger.warning('Disconnected from the network')
