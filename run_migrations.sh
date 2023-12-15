#!/usr/bin/env bash

read -p "Enter migration message: " msg
docker-compose exec web bash -c "cd insight_backend; poetry run alembic revision --autogenerate -m "$msg""
docker-compose exec web bash -c "cd insight_backend; poetry run alembic upgrade head"
