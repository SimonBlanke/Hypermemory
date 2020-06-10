dist:
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install:
	pip install .

develop:
	pip install -e .

reinstall:
	pip uninstall -y hypermemory
	rm -fr build dist hypermemory.egg-info
	python setup.py bdist_wheel
	pip install dist/*


test:
	pytest -p no:warnings -rfEX tests/ \
