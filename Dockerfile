FROM python:3.10 AS base

RUN apt-get update && apt-get upgrade -y

ENV POETRY_HOME=/opt/poetry POETRY_VIRTUALENVS_CREATE=false

RUN python -m venv ${POETRY_HOME}
RUN ${POETRY_HOME}/bin/pip install poetry==${POETRY_VERSION:-1.3}

# не добавляем весь ${POETRY_HOME}/bin в PATH, чтобы не тащить оттуда python/pip
RUN ln -s ${POETRY_HOME}/bin/poetry /usr/local/bin/poetry

# ставим prod зависимости
COPY ./poetry.lock ./pyproject.toml /usr/src/app/
WORKDIR /usr/src/app/
RUN poetry install --only main --no-root --no-interaction

##############
# prod образ #
##############

FROM base AS prod


#############
# dev-образ #
#############

FROM base AS dev
# доставляем dev-зависимости
RUN poetry install --no-root --no-interaction
COPY app /usr/src/app/
