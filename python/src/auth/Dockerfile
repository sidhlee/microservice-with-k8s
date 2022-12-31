# Build a base layer
FROM python:3.10-slim-bullseye

# Install OS dependencies 
# Combining all commands to keep them in the same run instruction
# and therefore, in one layer.
RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential default-libmysqlclient-dev \
  # recommended to pin the poetry version
  && pip install poetry==1.2.1 

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/

RUN \ 
  # Don't need virtualenv in an isolated container
  poetry config virtualenvs.create false \
  && if [ "$BUILD_ENVIRONMENT" = "deployment" ]; then \
      poetry install --no-dev --no-root; \
    else \
      poetry install --no-root; \
    fi

# Each docker command creates a cache layer.
# If there are no changes in pyproject.toml and poetry.lock files,
# but some changes in other files, docker build/push will start from this command
COPY . /app

# Just documenting which port is supposed to be exposed for the app
EXPOSE 5050

CMD ["python3", "./server.py"]
