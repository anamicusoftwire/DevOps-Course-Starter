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
CMD poetry run gunicorn --bind 0.0.0.0:${PORT:-80} "wsgi:run()"

FROM base as development
WORKDIR /todo_app
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]