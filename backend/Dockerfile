# Install uv
FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED True

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY uv.lock pyproject.toml ./

# Install dependencies
RUN uv sync --frozen --no-install-project --no-editable

COPY . .

# Sync the project
RUN uv sync --frozen --no-editable

FROM python:3.12-slim

# Copy the environment, but not the source code
COPY --from=builder /app /app

# Run the application
CMD gunicorn --bind :$PORT --workers 1 --threads 1 --timeout 0 main:app