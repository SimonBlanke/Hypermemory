dist:
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install:
	pip install .

develop:
	pip install -e .

reinstall:
	pip uninstall -y optimization_metadata
	rm -fr build dist optimization_metadata.egg-info
	python setup.py bdist_wheel
	pip install dist/*


test:
	pytest -p no:warnings -rfEX tests/ \
