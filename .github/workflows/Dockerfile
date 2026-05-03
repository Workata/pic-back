FROM python:3.14.4-alpine3.23

# * install uv
# * https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.11.8 /uv /uvx /bin/

# install Git to run pre-commit hooks
RUN apt-get update && \
    apt-get install -y --no-install-recommends git

# copy project files (see exlucded files in `.dockerignore`)
COPY . .

# sync packages (with dev deps)
RUN uv sync
