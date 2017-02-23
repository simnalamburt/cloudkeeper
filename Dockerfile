# Copyright 2017 Hyeon Kim
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

FROM python:3-alpine
MAINTAINER Hyeon Kim <simnalamburt@gmail.com>

# Update system
RUN apk upgrade --no-cache

# Prepare app environment
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install dependencies
COPY Pipfile.lock.txt /usr/src/app/
RUN pip install --no-cache-dir -r Pipfile.lock.txt

# Copy source codes
COPY . /usr/src/app

ENTRYPOINT ["python", "-m", "cloudkeeper"]
