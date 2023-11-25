# https://hub.docker.com/_/python - документация на образ python в dockerhub
FROM python:3.10

# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN apt-get update && apt-get install -y vim && pip install poetry==1.1.15

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . .
CMD ["./.venv/bin/python", "upload.py"]
