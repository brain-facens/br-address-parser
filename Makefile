install:
	pip install -e .

test:
	pip install -e .[dev]
	pytest -s
