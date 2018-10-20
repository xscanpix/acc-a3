FROM python:2.7-slim

MAINTAINER Svante Nilsson <svante.n@live.se>

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends

WORKDIR .

COPY requirements.txt requirements.txt

COPY . .

RUN pip install -r requirements.txt