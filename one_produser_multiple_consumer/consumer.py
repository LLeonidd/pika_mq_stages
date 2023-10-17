import logging
import argparse
from mq import MQ


logger = logging.getLogger('__file__')


def start_consumer(notif: dict):
    mq = MQ(
        host='rabbitmq_stage',
        port=5672,
    )
    mq.consume('', notif)


def parse_consumer_number() -> int:
    parser = argparse.ArgumentParser(description='Number of Consummer')
    parser.add_argument('consumer_number', metavar='cunsumer', type=int,
                        help='Number of Consummer')

    args = parser.parse_args()
    return args.consumer_number


if __name__ == '__main__':
    consumer_number = parse_consumer_number()
    start_consumer({'consumer': consumer_number})
