FROM python:3.10-slim-bullseye

RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential \
  && pip install poetry==1.2.1

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/

RUN \
  poetry config virtualenvs.create false\
  && poetry install --no-root;

COPY . /app

EXPOSE 8080

CMD ["python3", "./server.py"]