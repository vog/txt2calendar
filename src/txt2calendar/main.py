from __future__ import division, print_function, unicode_literals
__copyright__ = 'Copyright (C) Volker Diels-Grabsch <v@njh.eu>'

from .parse_t2c import parse_t2c
from .render_t2c import render_t2c
from .filter_events import filter_events
from sys import stderr

def read(filename):
    stderr.write('Reading from {filename} ...\n'.format(**locals()))
    with open(filename, 'rb') as f:
        return parse_t2c(f)

def write(filename, events):
    stderr.write('Writing to {filename} ...\n'.format(**locals()))
    with open(filename, 'wb') as f:
        render_t2c(f, events)

def main():
    events = read('test_input.t2c')
    write('test_output.t2c', events)
    events_filtered = filter_events(events)
    write('test_filtered.t2c', events_filtered)
    stderr.write('Done.\n')

if __name__ == '__main__':
    main()
