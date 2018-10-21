FROM python:2.7-slim

ENV FLASK_APP=myproject/app.py
ENV FLASK_ENV=development

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

EXPOSE 5000
EXPOSE 5672