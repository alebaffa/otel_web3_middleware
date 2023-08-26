PYTHON ?= . venv/bin/activate && python

all: setup

venv:
	[ -d venv ] || python -m venv --upgrade-deps venv

setup: venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

lint:
	$(PYTHON) -m isort --check --diff ./web3_server ./middleware
	$(PYTHON) -m black --check --diff ./web3_server ./middleware
	$(PYTHON) -m pylint ./web3_server ./middleware

lint/fix:
	$(PYTHON) -m isort ./web3_server ./middleware
	$(PYTHON) -m black ./web3_server ./middleware

mypy:
	$(PYTHON) -m mypy ./web3_server ./middleware

start:
	$(PYTHON) -m web3_server

start/jaeger:
	docker run --name jaeger   -e COLLECTOR_OTLP_ENABLED=true \
	-e DJAEGER_AGENT_HOST=0.0.0.0  -p 16686:16686 \
	-p 4317:4317   -p 4318:4318 \
	 jaegertracing/all-in-one:latest