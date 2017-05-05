#!/usr/bin/env python
import datetime
from influxdb import InfluxDBClient
import pika
import sys
import time


connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)


client = InfluxDBClient('influxdb', 8086, 'root', 'root', 'bakery')
client.create_database('bakery')

def create_measurement():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return [
        {
            "measurement": "orders",
            "tags": {
                "from": "client",
                "to": "assistant"
            },
            "time": st,
            "fields": {
                "value": 1
            }
        }
    ]


COUNTER=0
while True:
    COUNTER += 1
    message = ' '.join(sys.argv[1:]) or str(COUNTER) + " 1 Brownie"
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode = 2, # make message persistent
                          ))
    measurement = create_measurement()
    client.write_points(measurement)

    print("Sent and saved %r" % message)
    time.sleep(1)

connection.close()