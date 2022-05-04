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

It will expose 2 ports, one for the flask application (8888) and one for the RabbitMQ management interface (15672)
It will also start 2 worker containers.

When it runs, you can test it with several curl posts request and check it running in the Flower interface.

    for value in {1..50}
    do
        curl --data '{json}' -H 'Content-Type: application/json' 0.0.0.0:8888/api/process_data
    done

This will run 50 tasks, you can see in the flower [http://localhost:5556](http://0.0.0.0:5556/)
how the tasks are distributed between the worker instances.

You can also check the status of a specific task in flask: [http://localhost:8888/api/tasks/\<task-id\>](http://0.0.0.0:8888/api/tasks/<task-id>) 

The RabbitMQ interface [http://localhost:15673](http://0.0.0.0:15673/) with login:
- username: rabbit_user
- password: rabbit_password
