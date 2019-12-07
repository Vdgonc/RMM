#RabbitMQ Message Migrator
######Author: [Vinicius Justino](https://twitter.com/VdGonc)

---
####Description:
This is a simple tool for migrating messages on RabbitMQ server to
other RabbitMQ server.

###How to Works:
RMM queries the RabbitMQ API to enumerate queues, exchanges and routing keys,
and connect on server and consumes the queues and publish to the same queues as the other server.

###How to use:
#####Commands
    Usage:
        rmm.py -c config.json
    Flags:
        -h or --help 	help for rmm
        -c or --config 	Json path configuration

#####The json config:

    {
	"consumer": {
	  "host": "rabbit.dev.domain.com",
	  "port": 5672,
	  "virtualhost": "/",
	  "user": "masterUser",
	  "password": "s0M3P4$$W0rd!"
      },

      "publisher": {
        "host": "rabbit.prod.domain.com",
        "port": 5672,
        "virtualhost": "/",
        "user": "masterUser",
        "password": "s0M3P4$$W0rd!"
      },

      "server": {
        "host": "rabbit.dev.domain.com",
        "username": "masterUser",
        "password": "s0M3P4$$W0rd!",
        "virtualhost": "/"
      }
    }

###How to install:
#####Instaling dependences:
    pip3 install -r requirements.txt
