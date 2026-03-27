.PHONY: dev test lint format clean install

install:
	pip install -r requirements.txt
	pip install ruff black pytest pytest-asyncio

dev:
	uvicorn app.main:app --reload

test:
	pytest app/tests/ -v

lint:
	ruff check .
	black --check .

format:
	ruff check --fix .
	black .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
