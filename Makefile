install:
	pip3 install -r ./requirements.txt

install_dev:
	pip3 install -r ./requirements_dev.txt

lint:
	black --check chainbase_sdk/ tests/
	isort --check-only chainbase_sdk/ tests/
	flake8 chainbase_sdk/ tests/

format:
	black chainbase_sdk/ tests/
	isort chainbase_sdk/ tests/
	flake8 chainbase_sdk/ tests/

test:
	pytest -v

verify: lint test

e2e-test:
	pytest ./tests/e2e/e2e.py -v

clean:
	rm -rf build dist docs/build pip-wheel-metadata .mypy_cache .pytest_cache
	find . -regex ".*/__pycache__" -exec rm -rf {} +
	find . -regex ".*\.egg-info" -exec rm -rf {} +

package: clean install
	python3 -m pip install build && python3 -m build