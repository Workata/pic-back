# pic-back

[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/release/python-314/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Static Badge](https://img.shields.io/badge/type%20checked-mypy-039dfc)](http://mypy-lang.org/)
[![prek](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Contributions](https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square)

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

Optionally enable `prek` hooks
```sh
uv run prek install
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
