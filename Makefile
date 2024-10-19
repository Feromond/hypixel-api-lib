init:
	\
	python3 -m venv venv; \
	source venv/bin/activate; \
    pip install --upgrade pip; \
    pip install -r requirements.txt; \download_pip:
	./source  venv/bin/activate
