from time import sleep
import logging
from mq import MQ


logger = logging.getLogger('__file__')

def publish_message(msg=''):
    mq = MQ(
        host='rabbitmq_stage',
        port=5672,
    )
    msg_counter = 0
    while True:
        msg_frmt = f'{msg_counter}__{msg}'
        try:
            mq.produce(
                exchange='test_exchange',
                routing_key='',
                body=msg_frmt,
            )
            logger.warning(f'send message: {msg_frmt}')
            msg_counter += 1
            sleep(3)
        except KeyboardInterrupt:
            break
    mq.close()


if __name__ == '__main__':
    publish_message('test_message')
