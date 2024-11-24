import logging
from celery import Celery
import subprocess
from dotenv import dotenv_values
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = dotenv_values(".env") 

sqs_queue_url = config['sqs_queue_url']
aws_access_key = config['aws_access_key']
aws_secret_key = config['aws_secret_key']
aws_region = config['aws_region']

app = Celery(
    "celery_app",
    broker_url=f"sqs://{aws_access_key}:{aws_secret_key}@",
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_transport_options={
        "region": aws_region,
        "predefined_queues": {
            "celery": {
                "url": sqs_queue_url,
                "access_key_id": aws_access_key,
                "secret_access_key": aws_secret_key,
            }
        },
    },
    task_create_missing_queues=False,
)

def __get_worker_name():
    worker_name = subprocess.check_output(["cat", "/etc/hostname"])
    return (worker_name.decode('UTF-8').replace('\n',''))    

@app.task(name="consume_msg", bind=True)
def consume_msg(self,message):
    logger.info(F'workder_id = ${__get_worker_name()} , message = {message}')
    time.sleep(30) # 30 sec.