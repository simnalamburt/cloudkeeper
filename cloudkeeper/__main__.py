# coding: utf-8

# Copyright 2017 Hyeon Kim
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

from __future__ import print_function, unicode_literals, absolute_import
import sys
import time
import traceback

from .connection import IRCCloud


DELAY = 30


if __name__ == '__main__':
    try:
        while True:
            try:
                feed = IRCCloud()
                feed.auth()
                feed.connect()
            except KeyboardInterrupt:
                sys.exit()
            except:
                print(traceback.format_exc())
                print('Disconnected. Reconnecting in {} seconds.\n'.format(DELAY))
                time.sleep(DELAY)
                continue
    except KeyboardInterrupt:
        sys.exit()
