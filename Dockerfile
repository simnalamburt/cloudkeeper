FROM python:3-alpine
MAINTAINER Hyeon Kim <simnalamburt@gmail.com>

# Update system
RUN apk upgrade --no-cache

# Prepare app environment
WORKDIR /a
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT ["python", "-m", "cloudkeeper"]
