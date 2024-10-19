init:
	\
	python3 -m venv venv; \
	source venv/bin/activate; \
    pip install --upgrade pip; \
    pip install -r requirements.txt; \

build_local:
	echo "Building Local Library"
	pip3 install -e .
build:
	echo "Building Distribution Of Library"
	python3 setup.py bdist_wheel
destroy:
	echo "Uninstalling Local Build Of Library"
	pip3 uninstall geophysics_lib