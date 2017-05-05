#!/usr/bin/env python
import datetime
import pika
import sys
import time

from redis import Redis

redis = Redis(host='redis', port=6379)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


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

    redis.set("orders", str(COUNTER) + " Brownies")

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print("%r -  Sent and saved %r" % (st, message))
    time.sleep(1)

connection.close()