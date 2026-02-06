#!/usr/bin/env bash

set -e
set -x

# Alembic migration
alembic revision --autogenerate -m "autogenerate by docker file"
alembic upgrade head

python ./prestart.py
