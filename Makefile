# Copyright (C) Volker Diels-Grabsch <v@njh.eu>

.DELETE_ON_ERROR:

.PHONY: default
default: _build/

_build/:
	pip2 install -t $@ icalendar pyparsing

.PHONY: clean
clean:
	rm -rf _build/
