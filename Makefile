.PHONY: help dev test clean coverage

help:
	@echo "Usage:"
	@echo "  make dev     	- Start dev server"
	@echo "  make test     	- Run all tests"
	@echo "  make test-unit - Run unit tests"
	@echo "  make test-int  - Run integration tests"
	@echo "  make test-e2e  - Run end-to-end tests"
	@echo "  make clean    	- Remove cache files"

dev:
	uv run flask --app app.py run --debug

test: test-unit test-integration test-e2e

test-unit:
	uv run pytest tests/unit

test-integration:
	uv run pytest tests/integration

test-e2e:
	@echo "Starting E2E server..."
	rm -f test_e2e.db instance/test_e2e.db
	DATABASE_URL=sqlite:///test_e2e.db uv run flask --app app.py run --port 5005 & \
	SERVER_PID=$$!; \
	uv run pytest tests/e2e; \
	EXIT_CODE=$$?; \
	echo "Stopping E2E server (PID $$SERVER_PID)..."; \
	kill $$SERVER_PID || true; \
	exit $$EXIT_CODE

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -f *.db instance/*.db
