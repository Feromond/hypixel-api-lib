init:
	\
	python3 -m venv venv; \
	source venv/bin/activate; \
    pip install --upgrade pip; \
    pip install -r requirements.txt; \download_pip:
	./source  venv/bin/activate
build_local:
	echo "Building Local Library"
	pip3 install -e .
build:
	echo "Building Distribution Of Library"
	python3 setup.py bdist_wheel