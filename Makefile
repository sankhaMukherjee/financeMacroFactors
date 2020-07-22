.PHONY: grantPermissions clean build venv docs docs1 tests

grantPermissions:
	chmod 766 bin/*

clean:
	bin/clean.sh

build:
	python3 setup.py bdist_wheel
	bin/clean.sh

firstRun:
	chmod 766 bin/*
	bin/vEnv.sh
	bin/makeGit.sh
	bin/clean.sh

install:
	pip3 install -e .

tests:
	python3 -m pytest tests

docs:
	bin/docs.sh
