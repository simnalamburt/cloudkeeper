FROM python:3-alpine
MAINTAINER Hyeon Kim <simnalamburt@gmail.com>

# Update system
RUN apk upgrade --no-cache

# Prepare app environment
WORKDIR /a
COPY . .
RUN pip install .

ENTRYPOINT ["python", "-m", "cloudkeeper"]
