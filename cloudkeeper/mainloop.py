# coding: utf-8
from __future__ import unicode_literals, absolute_import
import os
import sys
import time
import signal
import traceback
import logging

from .connection import IRCCloud


def mainloop(delay=30):
    '''
    Tries to connect to the IRCCloud server infinitely.

    delay: Reconnection delay in seconds
    '''

    # Set log level
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Consider SIGINT as a goodbye signal
    handler = lambda sig, frame: (logging.info('Recieved SIGINT, turning off the process. Goodbye!'), sys.exit(0))
    signal.signal(signal.SIGINT, handler)

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
        connection = IRCCloud()

        logging.info('Starting authentication ...')
        sys.stdout.flush()
        result = connection.auth(email, password)
        if result is None:
            logging.error('Authentication failed. Perhaps wrong email/password combination.')
            sys.exit(1)
        logging.info('Authentication completed.')

        try:
            connection.connect(
                lambda: logging.info('Connection created.'),
                lambda: logging.warning('Disconnected from the network'))
        except SystemExit:
            raise
        except:
            logging.error('Unhandled exception occurred:')
            logging.error(traceback.format_exc())
            logging.error('Disconnected. Reconnecting in {} seconds.'.format(delay))
            time.sleep(delay)
