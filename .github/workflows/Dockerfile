FROM python:3.14.4-alpine3.23

# * install uv
# * https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.11.8 /uv /uvx /bin/

RUN apk add --no-cache git

# copy project files (see exlucded files in `.dockerignore`)
COPY . .

# sync packages (with dev deps)
RUN uv sync
