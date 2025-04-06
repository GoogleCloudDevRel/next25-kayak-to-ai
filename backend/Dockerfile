# Install uv
FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED True

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY uv.lock pyproject.toml ./

# Install dependencies
RUN uv sync --frozen --no-install-project

COPY . .

RUN uv sync --frozen

# FROM python:3.12-slim

# COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["gunicorn", "main:app", "--bind :$PORT", "--workers 1", "--threads 1", "--timeout 0"]