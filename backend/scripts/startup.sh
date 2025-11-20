#!/usr/bin/env bash

docker run -d \
      --name swag_db \
      -e POSTGRES_USER=swag \
      -e POSTGRES_PASSWORD=qwe123 \
      -e POSTGRES_DB=db \
      -p 5432:5432 \
      postgres