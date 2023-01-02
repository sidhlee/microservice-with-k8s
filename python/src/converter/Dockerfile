FROM python:3.10-slim-bullseye

RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  # ffmpeg is a dependency of moviepy
  build-essential ffmpeg\ 
  && pip install poetry==1.3.1

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/

RUN \
  poetry config virtualenvs.create false\
  && poetry install --no-root;

COPY . /app

# No need to expose port for consumers, which doens't take request
# but actively takes the message from the queue

CMD ["python3", "./consumer.py"]
