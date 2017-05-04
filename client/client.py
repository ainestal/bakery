#!/usr/bin/env python
import pika
import sys
import time

COUNTER=0

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


while True:
    COUNTER += 1
    message = ' '.join(sys.argv[1:]) or str(COUNTER) + " 2 Brownies"
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode = 2, # make message persistent
                          ))
    print(" Sent %r" % message)
    time.sleep(1)

connection.close()