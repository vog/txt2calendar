from __future__ import division, print_function, unicode_literals
__copyright__ = 'Copyright (C) Volker Diels-Grabsch <v@njh.eu>'

from re import split
from re import match

def parse_blocks(fileobj):
    input_bytes = fileobj.read()
    assert isinstance(input_bytes, bytes)
    input_unicode = input_bytes.decode('utf-8')
    for raw_block in split(r'\n\n+', input_unicode):
        block = raw_block.strip('\n')
        if block != '':
            yield block

def parse_linegroups(block):
    indent = ' '
    linegroup = None
    for raw_line in block.split('\n'):
        if raw_line.startswith(indent):
            if linegroup is None:
                linegroup = {
                    'first_line': '',
                    'additional_lines': [],
                }
            linegroup['additional_lines'].append(raw_line[len(indent):])
        else:
            if linegroup is not None:
                yield linegroup
            linegroup = {
                'first_line': raw_line,
                'additional_lines': [],
            }
    if linegroup is not None:
        yield linegroup

def parse_field(linegroup):
    orig_first_line = linegroup['first_line']
    additional_lines = linegroup['additional_lines']
    m = match(r'([^:]+):\s*(.*)$', orig_first_line)
    if m is None:
        return {
            'field_name': 'unknown',
            'first_line': orig_first_line,
            'additional_lines': additional_lines,
        }
    field_name, first_line = m.groups()
    return {
        'field_name': field_name,
        'first_line': first_line,
        'additional_lines': additional_lines,
    }

def parse_record(block):
    return [
        parse_field(linegroup)
        for linegroup in parse_linegroups(block)
    ]

def parse_records(fileobj):
    for block in parse_blocks(fileobj):
        yield parse_record(block)
