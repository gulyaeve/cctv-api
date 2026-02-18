FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /src

# Install dependencies
RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen

# RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
#       pip install -r requirements.txt

# COPY requirements.txt ./
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

COPY . .

# Place executables in the environment at the front of the path
ENV PATH="/src/.venv/bin:$PATH"

# RUN alembic upgrade head

RUN chmod a+x /src/docker/entry_point.sh
# ENTRYPOINT ["python", "run.py"]
# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT ["/src/docker/entry_point.sh"]
