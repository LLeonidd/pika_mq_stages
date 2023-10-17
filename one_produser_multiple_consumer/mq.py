import logging
import pika
from functools import partial


logger = logging.getLogger('__file__')


class MQ:
    def __init__(
        self,
        host: str,
        port: int,
    ):

        parameters = pika.ConnectionParameters(host,
                                               port,
                                               '/',)

        self.exchange_name = "test_exchange"
        self.conn = pika.BlockingConnection(parameters)
        self.channel = self.conn.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')

        # for consumer queue
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name)

    def callback(self, ch, method, properties, body: bytes, notif=None) -> None:
        data = body.decode('utf8')
        logger.warning(f'Recive message: {data} {notif}')

    def consume(self, queue: str,  notif={}) -> None:
        self.channel.basic_consume(
            on_message_callback=partial(self.callback, notif=notif),
            queue=self.queue_name,
            auto_ack=True,
        )
        self.channel.start_consuming()

    def produce(self, exchange: str, routing_key: str, body: str) -> None:
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
        )

    def close(self):
        self.conn.close()