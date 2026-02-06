#!/usr/bin/env bash

set -e
set -x

# Alembic migration
alembic upgrade head

python ./prestart.py
