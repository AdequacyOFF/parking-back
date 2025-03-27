FROM registry-int.flydata.ru/devops/docker/images/python:3.10 AS base

# ставим prod зависимости
COPY ./poetry.lock ./pyproject.toml /usr/src/app/
WORKDIR /usr/src/app/
COPY . /usr/src/app/
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
