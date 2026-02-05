FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies
RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen

COPY . /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

RUN alembic upgrade head

# ENTRYPOINT ["python", "run.py"]
# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]