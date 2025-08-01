-include .env

help:
	@awk 'BEGIN {FS = ":.*#"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?#/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^#@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

up: ## compose up
	@docker compose up --wait -d

down: ## compose down
	@docker compose down

stop: ## compose stop
	@docker compose  stop

venv: # create/update venv
	@uv sync --frozen --all-packages --all-groups

lint: # run linters and formatters
	@uv run ruff check . --fix && \
	uv run isort . --check-only && \
	uv run ruff format --check . && \
	uv run mypy .

lint-fix: # run linters and formatters with fix
	@uv run ruff check . && \
	uv run isort . && \
	uv run ruff format . && \
	uv run mypy .

test-env: # create test environment
	cp .env.example .env

test-dev: test-env venv up # run project


test: # run tests
	@echo "Building image..."
	@docker compose run --quiet --build --rm tester
	@docker image rm $$(docker images -q $(ENV_PROJECT_NAME)-tester 2>/dev/null) 2>/dev/null || true

