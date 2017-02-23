# coding: utf-8

# Copyright 2017 Hyeon Kim
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

from __future__ import unicode_literals, absolute_import
import sys
import time
import signal
import traceback
import binascii
import logging
from base64 import b64decode
if sys.version_info >= (3,):
    import pickle
else:
    import cPickle as pickle

from .ask import ask
from .connection import IRCCloud


#
# Constants
#
DELAY = 30


def main():
    '''
    Main logic. Asks credentials to the user and tries to connect to the
    IRCCloud server infinitely.
    '''

    # Set log level
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Consider SIGINT as a goodbye signal
    handler = lambda sig, frame: (logging.info('Recieved SIGINT, turning off the process. Goodbye!'), sys.exit(0))
    signal.signal(signal.SIGINT, handler)

    # Ask credentials to the user
    if len(sys.argv) > 2:
        logging.error('Too many arguments have been supplied.')
        sys.exit(1)
    elif len(sys.argv) < 2:
        # No credentials supplied
        data = ask()
    else:
        # Credentials have been supplied as a argument
        serialized = sys.argv[1]
        try:
            pickled = b64decode(serialized)
            data = pickle.loads(pickled)
        except (EOFError, ValueError, KeyError, binascii.Error, pickle.UnpicklingError) as e:
            logging.error('Wrong arguments have been supplied. ({})'.format(e))
            sys.exit(1)

    # Try to connect to the server infinitely
    while True:
        connection = IRCCloud()

        logging.info('Starting authentication ...')
        sys.stdout.flush()
        result = connection.auth(*data)
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
            logging.error('Disconnected. Reconnecting in {} seconds.'.format(DELAY))
            time.sleep(DELAY)


if __name__ == '__main__':
    main()
