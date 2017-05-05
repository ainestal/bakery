#!/usr/bin/env python
import datetime
from influxdb import InfluxDBClient
import pika
import time


class Client:
    queue_of_clients = []
    notebook = []

    def __init__(self):
        self.queue_of_clients = self.setup_queue_connection()
        self.notebook = self.setup_db_connection()

    @staticmethod
    def setup_queue_connection():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        queue_of_clients = connection.channel()
        queue_of_clients.queue_declare(queue='task_queue', durable=True)
        return queue_of_clients

    @staticmethod
    def setup_db_connection():
        notebook = InfluxDBClient('influxdb', 8086, 'root', 'root', 'bakery')
        notebook.create_database('bakery')
        return notebook

    @staticmethod
    def create_measurement():
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return [
            {
                "measurement": "orders",
                "tags": {
                    "from": "client",
                    "to": "assistant",
                    "product": "brownie"
                },
                "time": st,
                "fields": {
                    "value": 1
                }
            }
        ]

    def place_order_in_queue(self, amount=1, product='Brownie'):
        message = "%r %r" % (amount, product)
        self.queue_of_clients.basic_publish(exchange='',
                                            routing_key='task_queue',
                                            body=message,
                                            properties=pika.BasicProperties(
                                                delivery_mode=2,  # make message persistent
                                            ))

    def write_order_in_notebook(self):
        measurement = self.create_measurement()
        self.notebook.write_points(measurement)


def main():
    client = Client()
    while True:
        client.place_order_in_queue()
        time.sleep(1)

if __name__ == '__main__':
    main()
