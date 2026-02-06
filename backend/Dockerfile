FROM python:3.14.2-slim AS python-base

ENV PYTHONBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.1.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH" \
    PYTHONPATH="$POETRY_HOME:$PYTHONPATH"

FROM python-base AS builder

WORKDIR $PYSETUP_PATH

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential


COPY ./poetry.lock ./pyproject.toml ./


RUN pip install --target $POETRY_HOME "poetry==$POETRY_VERSION"
RUN poetry install --no-root --only main

FROM python-base AS dev

WORKDIR $PYSETUP_PATH

COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH
COPY --from=builder $POETRY_HOME $POETRY_HOME
RUN poetry install --no-root --with dev

WORKDIR /app
ENV ENV_TYPE=dev
ENV PYTHONPATH="/app:$PYTHONPATH"


EXPOSE 8000
CMD ["uvicorn", "--host", "0.0.0.0", "--reload", "src.main:app"]

FROM python-base AS production
ENV ENV_TYPE=production

COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

WORKDIR /app

COPY ./alembic.ini ./
COPY ./startup.sh ./startup.sh
COPY ./src ./src
CMD ["uvicorn", "src.main:app"]
