# bakery
This distributed bakery lives on top of docker

It's an example of a producers-consumers using microservices.

## What it does
In this shop there are:
 - clients: they place bakery orders
 - assistants: they talk to the clients and to the baker
 - baker: Not implemented yet
 
## How to run it
```$ docker-compose build && docker-compose up -d```

## How to see what's going on
Use a browser to connect to
 - http://localhost:3000 to access [Grafana](https://grafana.com/). You can connect it to InfluxDB as a source, use the URL of InfluxDB, the one in the next point
 - http://localhost:8086 to access [InfluxDB](https://www.influxdata.com/)
 - http://localhost:8080 to access [Rabbitmq](https://www.rabbitmq.com/) management console
 
 ## How to enjoy it
 You can scale the number of containers you run of each type. That makes things quite interesting. Some examples:
 ```
 $ docker-compose scale client=5
 $ docker-compose scale assistant=2
 ```
 
