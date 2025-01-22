FROM python:3.12

LABEL tech.tomy.docker.k.backend="0.8.0"
LABEL maintainer="Tomy Hsieh @tomy0000000"

WORKDIR /usr/src/k-backend
EXPOSE 8000

# Install pip & poetry
RUN pip install --upgrade pip poetry

# Copy dependencies
COPY pyproject.toml poetry.lock /usr/src/k-backend/

# Install Dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy Application
COPY . /usr/src/k-backend
