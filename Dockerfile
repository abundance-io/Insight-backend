# Dockerfile

# pull the official docker image
FROM python:3.11.1-slim

# set work directory
WORKDIR /insight_backend

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY poetry.lock .
COPY pyproject.toml .

RUN pip install poetry
RUN poetry install

# copy project
COPY . .
