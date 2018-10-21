FROM python:2.7-slim


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

EXPOSE 5000
EXPOSE 5672