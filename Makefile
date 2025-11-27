.PHONY: check
check:
	@echo "Running static checks via pre-commit..."
	uv run pre-commit run --all-files

.PHONY: test
test:
	@echo "Running unit tests..."
	uv run pytest --cov=pic_back --cov-report term-missing

.PHONY: run
run:
	@echo "Running fast api application..."
	uv run fastapi dev pic_back/main.py


.PHONY: run-docker
run-docker:
	@echo "Running containerized fast api application..."
	docker build . --tag pic-back-image
	docker run pic-back-image
