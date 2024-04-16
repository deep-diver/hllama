lint:
	pip install ruff
	pip install pre-commit
	pre-commit install
	pre-commit run --all-files

doc:
	pip install -U pdoc3
	rm -rf docs
	pdoc --html ./src/hllama/ --output-dir docs
	mv docs/hllama/* docs/
	rm -rf docs/hllama

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