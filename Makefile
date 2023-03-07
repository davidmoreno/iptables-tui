all:
	@echo "run   -- Runs the app"
	@echo "setup -- Setups the environment"

.PHONY: setup
setup:
	python3 -m venv env
	env/bin/pip install -r requirements.txt

env:

FILE=examples/01.iptables

run: env 
	env/bin/python3 app.py ${FILE}

