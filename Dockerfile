FROM python:3.10.0-slim-buster as base

ARG ENVIRONMENT

ENV FLASK_ENV=${FLASK_ENV}

RUN pip install poetry
COPY . /todo_app
EXPOSE 5000

FROM base as production
WORKDIR /todo_app
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install && poetry add gunicorn
ENTRYPOINT ["poetry", "run", "gunicorn", "--config", "config_gunicorn", "todo_app.app:create_app()"]

# FROM base as development
# WORKDIR /todo_app
# COPY poetry.lock .
# COPY pyproject.toml .
# RUN poetry install
# ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]