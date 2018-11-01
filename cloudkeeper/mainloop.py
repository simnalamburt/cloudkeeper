# coding: utf-8
from __future__ import unicode_literals, absolute_import
import os
import sys
import time
import signal
import traceback
import logging

from .connection import auth, connect

logger = logging.getLogger(__name__)


def sigint_handler(sig, frame):
    logger.info('Recieved SIGINT, turning off the process. Goodbye!')
    sys.exit(0)


def mainloop(delay=30):
    '''
    Tries to connect to the IRCCloud server infinitely.

    delay: Reconnection delay in seconds
    '''

    # Set log level
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Consider SIGINT as a goodbye signal
    signal.signal(signal.SIGINT, sigint_handler)

    # Retrieve credentials from the config file, or ask it to the user
    email = os.environ.get('CLOUDKEEPER_EMAIL')
    password = os.environ.get('CLOUDKEEPER_PASSWORD')
    if email is None:
        logger.error('Please set CLOUDKEEPER_EMAIL environment variable')
        sys.exit(1)
    if password is None:
        logger.error('Please set CLOUDKEEPER_PASSWORD environment variable')
        sys.exit(1)

    # Try to connect to the server infinitely
    while True:
        session, url = auth(email, password)
        if session is None:
            logger.error('Authentication failed')
            sys.exit(1)

        try:
            connect(session, url)
        except SystemExit:
            raise
        except Exception:
            logger.error('Unhandled exception occurred:\n{}'.format(traceback.format_exc()))
            logger.error('Disconnected, reconnecting in {} seconds'.format(delay))
            time.sleep(delay)
