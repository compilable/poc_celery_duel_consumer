# Dockerfile
FROM python:3.12

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

CMD celery --app=worker.app worker --pool=solo --concurrency=3 --loglevel=INFO --queues=celery