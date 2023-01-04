test:
	poetry run python -m pytest
test-ci:
	poetry run python -m pytest --cov-report=xml
test-no-cov:
	poetry run python -m pytest --no-cov