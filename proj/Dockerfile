FROM python:2.7-slim

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

RUN apt-get install rabbitmq-server

COPY . /code/
WORKDIR /code/

EXPOSE 5000
EXPOSE 5672