FROM python:2.7-slim

MAINTAINER Svante Nilsson <svante.n@live.se>

ENV INSTALL_PATH /proj
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN pip install --editable .