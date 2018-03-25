from __future__ import division, print_function, unicode_literals
__copyright__ = 'Copyright (C) Volker Diels-Grabsch <v@njh.eu>'

def render_str(o, s):
    o(s.encode('utf-8'))

def render_record(o, record):
    for field in record:
        field_name = field['field_name']
        first_line = field['first_line']
        additional_lines = field['additional_lines']
        render_str(o, field_name)
        render_str(o, ':')
        if first_line != '':
            render_str(o, ' ')
            render_str(o, first_line)
        render_str(o, '\n')
        for line in additional_lines:
            render_str(o, ' ')
            render_str(o, line)
            render_str(o, '\n')

def render_records(fileobj, records):
    o = fileobj.write
    for i, record in enumerate(records):
        if i != 0:
            render_str(o, '\n')
        render_record(o, record)
