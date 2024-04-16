lint:
	pip install ruff
	pip install pre-commit
	pre-commit install
	pre-commit run --all-files

test:
	pytest

publish:
	python setup.py bdist_wheel
	twine upload dist/*
	rm -rf dist
	rm -rf src/hllama.egg-info
	rm -rf build
	
clean:
	rm -rf dist
	rm -rf src/hllama.egg-info
	rm -rf build