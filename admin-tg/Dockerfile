FROM python:3.14.0-slim-trixie

#RUN apt-get update && apt-get install -y \
#    gcc \
#    g++ \
#    python3-dev \
#    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml /app/

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR='/var/cache/pypoetry'
ENV POETRY_HOME='/usr/local'
ENV POETRY_VERSION=2.1.4

RUN pip install --upgrade pip wheel "poetry==2.1.4"
RUN poetry install

COPY . /app/
