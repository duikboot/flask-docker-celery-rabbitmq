DC = docker-compose
ENV = Dev


run:
	APP_ENV=$(ENV) $(DC) up

up: run

build:
	APP_ENV=$(ENV) $(DC) build

