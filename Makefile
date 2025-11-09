.PHONY: check
check:
	@echo "Running static checks..."
	@echo "Running mypy - type checker"
	uv run mypy .
	@echo "Running ruff - formatter + linter"
	uv run ruff check --fix
	uv run ruff format

.PHONY: test
test:
	@echo "Running unit tests..."
	uv run pytest --cov=pic_back .

.PHONY: run
run:
	@echo "Running fast api application"
	uv run fastapi dev pic_back/main.py
