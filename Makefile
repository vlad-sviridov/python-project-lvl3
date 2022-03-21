install:
	poetry install

test:
	poetry run pytest tests -cov=page_loader

lint:
	poetry run flake8 page_loader

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

.PHONY: insall test lint selfcheck build package-install
