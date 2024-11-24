import logging

from worker import app
from random_word import RandomWords

random = RandomWords()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_dummy_msg(message):
    async_result = app.send_task("consume_msg",[message])
    logger.info(F'message = {message}, consumer={"consume_msg"} , sent_status = {async_result}')

if __name__ == '__main__':
    send_dummy_msg(F'Word for the msg: {random.get_random_word()}')