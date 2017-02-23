# coding: utf-8

# Copyright 2017 Hyeon Kim
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

from __future__ import unicode_literals
import toml

def try_open(path):
    try:
        return open(path)
    except IOError:
        return None

def config():
    handle = try_open('secret.toml') or try_open('/etc/cloudkeeper/secret.toml')
    if handle is None:
        return None

    with handle as file:
        config = toml.loads(file.read())

    email = config.get('email')
    password = config.get('password')

    if email is None or password is None:
        return None
    return (email, password)
