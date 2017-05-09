#!/usr/bin/env python
import datetime
import pika
import time


class Assistant:
    queue_of_clients = []

    def __init__(self):
        self.queue_of_clients = self.setup_queue_connection()
        print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(self, ch, method, properties, body):
        self.do_something()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def do_something():
        time.sleep(1)

    @staticmethod
    def setup_queue_connection():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        queue_of_clients = connection.channel()
        queue_of_clients.queue_declare(queue='customer_queue', durable=True)
        return queue_of_clients

    def wake_up(self):
        self.watch_customer_queue()

    def watch_customer_queue(self):
        self.queue_of_clients.basic_qos(prefetch_count=1)
        self.queue_of_clients.basic_consume(self.callback, queue='customer_queue')
        self.queue_of_clients.start_consuming()


def main():
    Assistant().wake_up()

if __name__ == '__main__':
    main()
