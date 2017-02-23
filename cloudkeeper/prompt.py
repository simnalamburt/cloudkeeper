# coding: utf-8

# Copyright 2017 Hyeon Kim
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

from __future__ import print_function, unicode_literals
import sys
import signal
import getpass
from base64 import b64encode
if sys.version_info >= (3,):
    import pickle
else:
    import cPickle as pickle
    input = raw_input


def ask():
    '''
    Ask login credentials to the user.
    '''
    print('Logging in to the IRCCloud server\n', file=sys.stderr)

    # Get email address
    print('     email : ', end='', file=sys.stderr)
    sys.stderr.flush()
    email = input()

    # Get password
    print('  password : ', end='', file=sys.stderr)
    sys.stderr.flush()
    password = getpass.getpass('')

    print(file=sys.stderr)
    return (email, password)


if __name__ == '__main__':
    # Consider SIGINT as a goodbye signal
    handler = lambda sig, frame: (print('\n\nGoodbye!', file=sys.stderr), sys.exit(0))
    signal.signal(signal.SIGINT, handler)

    # Ask the credentials
    data = ask()

    # Serialize the data
    serialized = b64encode(pickle.dumps(data, 2)).decode()
    print(serialized)
    print('\x1b[34mPassing the data to the original process\x1b[0m', file=sys.stderr)
