.PHONY: help dev test clean coverage

help:
	@echo "Usage:"
	@echo "  make dev      - Start the Flask development server"
	@echo "  make test     - Run pytest suite"
	@echo "  make clean    - Remove python cache files"
	@echo "  make coverage - Run tests and show coverage"

dev:
	uv run flask --app app.py run --debug

test: test-unit test-integration #test-e2e

test-unit:
	PYTHONPATH=. uv run pytest tests/unit

test-integration:
	PYTHONPATH=. uv run pytest tests/integration

test-e2e:
	@echo "Starting E2E server..."
	FLASK_ENV=testing FLASK_DEBUG=0 PYTHONPATH=. uv run flask --app app.py run --port 5005 & \
	SERVER_PID=$$!; \
	PYTHONPATH=. uv run pytest tests/e2e; \
	EXIT_CODE=$$?; \
	echo "Stopping E2E server (PID $$SERVER_PID)..."; \
	kill $$SERVER_PID || true; \
	exit $$EXIT_CODE

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	
coverage:
	uv run pytest --cov=app tests/