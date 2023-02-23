all:
	@echo "run   -- Runs the app"
	@echo "setup -- Setups the environment"

.PHONY: setup
setup:
	python3 -m venv env
	pip install -f requirements.txt

env:

run: env 
	env/bin/python3 app.py

