# POC [ Running Celery worker on multiple Docker instances - Duplicate Consumption ]

A POC To test running Celery workes pointing to the same SQS (Standard) **won't** result in processing the same message.

## SQS (Standard) setup:
- Name : celery_test
- Default visibility timeout : 30 Seconds
- Receive message wait time : 20 Seconds
- Delivery delay : 0 Seconds
- Access policy: 

```
{
  "Version": "2012-10-17",
  "Id": "__default_policy_ID",
  "Statement": [
    {
      "Sid": "__owner_statement",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::XXXXX:XXXX"
      },
      "Action": "SQS:*",
      "Resource": "arn:aws:sqs:XXXXX:XXXXX:celery_test"
    }
  ]
}
```
## AWS configuration:
- To be added to `.env` : 
```
sqs_queue_url=""
aws_access_key=""
aws_secret_key=""
aws_region=""
```

# Install dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Start worker:
- Using Docker compose: 
```
docker-compose up -d
```
- Running isolated worker:
```
celery --app=worker.app worker --pool=solo --concurrency=1 --loglevel=INFO --queues=celery
```
- Starting individual Docker containers:
```
docker build -t celery_app .
docker run --name worker_1 -d celery_app
docker run --name worker_2 -d celery_app
```

## Sending the message:
- Using python:
```
python3 sender.py
```



