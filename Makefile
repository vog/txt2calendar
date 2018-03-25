# Copyright (C) Volker Diels-Grabsch <v@njh.eu>

.DELETE_ON_ERROR:

.PHONY: default
default: check

_build/:
	pip2 install -t $@ icalendar pyparsing pytest

.PHONY: check
check: _build/
	@PYTHONPATH=_build python2 -Bm pytest --strict -p no:cacheprovider -vv -- src
	@echo ok

.PHONY: clean
clean:
	rm -rf _build/
