FROM python:3.12

LABEL tech.tomy.docker.kayman="0.10.0"
LABEL maintainer="Tomy Hsieh @tomy0000000"

WORKDIR /usr/src/kayman
EXPOSE 8000

# Install pip & poetry
RUN pip install --upgrade pip poetry

# Copy dependencies
COPY backend/pyproject.toml backend/poetry.lock /usr/src/kayman/

# Install Dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy Application
COPY backend/ /usr/src/kayman

# Run Application
ENTRYPOINT [ "uvicorn", "kayman.main:app", "--host", "0.0.0.0", "--port", "8000" ]
