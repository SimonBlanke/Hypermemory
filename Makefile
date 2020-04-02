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
	cd tests/; \
		pytest test_memory.py -p no:warnings; \
		pytest test_memory_helpers.py -p no:warnings
