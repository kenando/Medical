.PHONY: start
start:
	python3 app.py

.PHONY: install
install:
	pip3 install -r requirements.txt

.PHONY: fmt
fmt:
	black src/
	isort src/

.PHONY: lint
lint:
	flake8 src/
	mypy src/

