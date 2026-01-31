FROM python:3.14.0-slim as buider

#RUN apt-get update && apt-get install -y \
#    gcc \
#    g++ \
#    python3-dev \
#    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

COPY ./poetry.lock ./pyproject.toml /app/
RUN pip install "poetry==2.1.4" \
    && poetry install --no-root --only main

FROM python:3.14.0-slim as production

WORKDIR /app
COPY --from=buider /app/.venv /app/.venv
COPY . .
