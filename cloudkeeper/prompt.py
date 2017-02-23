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
import getpass
if sys.version_info < (3,):
    input = raw_input

def ask():
    print('Logging in to the IRCCloud server\n', file=sys.stderr)

    # Get email address
    print('     email : ', end='', file=sys.stderr)
    sys.stderr.flush()
    email = input()

    # Get password
    print('  password : ', end='', file=sys.stderr)
    sys.stderr.flush()
    password = getpass.getpass('')

    return (email, password)
