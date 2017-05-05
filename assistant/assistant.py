#!/usr/bin/env python
import datetime
import pika
import time


class Assistant:
    queue_of_clients = []

    def __init__(self):
        self.queue_of_clients = self.setup_queue_connection()
        print(' [*] Waiting for messages. To exit press CTRL+C')

    @staticmethod
    def setup_queue_connection():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        queue_of_clients = connection.channel()
        queue_of_clients.queue_declare(queue='task_queue', durable=True)
        return queue_of_clients

    @staticmethod
    def callback(ch, method, properties, body):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print("%r - Received %r" % (st, body))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        time.sleep(0.1)

    def consume(self):
        self.queue_of_clients.basic_qos(prefetch_count=1)
        self.queue_of_clients.basic_consume(self.callback, queue='task_queue')
        self.queue_of_clients.start_consuming()


def main():
    Assistant().consume()

if __name__ == '__main__':
    main()

