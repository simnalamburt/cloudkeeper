# coding: utf-8
from __future__ import unicode_literals, absolute_import
import os
import sys
import time
import signal
import traceback
import logging

from .connection import auth, connect


def sigint_handler(sig, frame):
    logging.info('Recieved SIGINT, turning off the process. Goodbye!')
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
        logging.error('Please set CLOUDKEEPER_EMAIL environment variable')
        sys.exit(1)
    if password is None:
        logging.error('Please set CLOUDKEEPER_PASSWORD environment variable')
        sys.exit(1)

    # Try to connect to the server infinitely
    while True:
        logging.info('Starting authentication')
        sys.stdout.flush()
        session = auth(email, password)
        if session is None:
            logging.error('Authentication failed')
            sys.exit(1)
        logging.info('Authentication completed')

        try:
            connect(
                session,
                on_succeeded=lambda: logging.info('Connection created'),
                on_disconnect=lambda: logging.warning('Disconnected from the network'),
            )
        except SystemExit:
            raise
        except Exception:
            logging.error('Unhandled exception occurred:')
            logging.error(traceback.format_exc())
            logging.error('Disconnected, reconnecting in {} seconds'.format(delay))
            time.sleep(delay)
