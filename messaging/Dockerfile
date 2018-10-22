FROM python:2.7-slim

ENV FLASK_APP=tasks.py
ENV FLASK_ENV=development

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY ./tasks.py ./app

EXPOSE 5000
EXPOSE 5672
EXPOSE 15672
EXPOSE 6379
EXPOSE 5555