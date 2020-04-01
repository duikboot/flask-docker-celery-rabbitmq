# flask-docker-celery-rabbitmq

This repository is for running a simple dummy flask application in a docker environment.

It uses:
- Flask
- Celery
- Flower
- Rabbitmq
- PostgreSQL (not doing anything, though)


## Prerequisites
Make sure you have docker and docker-compose installed.

## Running
Clone this repository and navigate into it in your terminal.
Run in development mode, so set APP_ENV environment to Dev

    APP_ENV=Dev docker-compose up --build

It will expose 2 ports, one for the flask application (8000) and one for the RabbitMQ management interface (15672)

When it runs, you can test it with several curl posts request and check it running in the Flower interface.

    curl --data '{json}' -H 'Content-Type: application/json' 0.0.0.0:8000/api/process_data

It will return a task_id, which you can search for in Flower [http://localhost:8888](http://0.0.0.0:8888/tasks).

The RabbitMQ interface [http://localhost:15672](http://0.0.0.0:15672/) with login:
- username: rabbit_user
- password: rabbit_password
