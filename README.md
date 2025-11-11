# pic-back

Backend for pic-pages (tomtol) application.

### Development

Install uv
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify uv installation
```sh
uv --version
```

Sync packages
```sh
uv sync
```

Run static checks (via precommit)
```sh
make check
```

Run unit tests and check coverage
```sh
make test
```

Optionally enable `pre-commit` hooks
```sh
uv run pre-commit install
```

### Containerization

Build and run docker image directly
```sh
docker build . --tag pic-back-image
docker run pic-back-image
```

Build and run application via `docker-compose`
```sh
docker compose build
docker compose up fastapi
```
