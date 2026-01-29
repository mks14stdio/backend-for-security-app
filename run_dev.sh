#!/usr/bin/env bash

export DB_USER=dev
export DB_PASSWORD=testtest
export DB_NAME=db_name


docker compose -f docker-compose.yml watch
