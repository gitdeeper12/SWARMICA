# SWARMICA Makefile

.PHONY: install test lint format clean build deploy

install:
	pip install -e .

test:
	pytest tests/ -v --cov=swarmica

test-benchmark:
	pytest tests/benchmark/ -v --benchmark-only

lint:
	flake8 swarmica/ tests/
	mypy swarmica/

format:
	black swarmica/ tests/
	isort swarmica/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

build: clean
	python -m build

deploy: build
	twine upload dist/*

docker-build:
	docker build -t swarmica:latest .

docker-run:
	docker run -it --rm swarmica:latest

help:
	@echo "Available commands:"
	@echo "  make install      - Install package in development mode"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make build        - Build distribution packages"
	@echo "  make deploy       - Deploy to PyPI"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
