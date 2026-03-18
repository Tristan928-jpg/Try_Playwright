.PHONY: venv install playwright test

venv:
	python -m venv .venv

install:
	.venv\Scripts\python -m pip install --upgrade pip
	.venv\Scripts\pip install -r requirements.txt
	.venv\Scripts\python -m playwright install

test:
	.venv\Scripts\python -m pytest -v

all: venv install test

