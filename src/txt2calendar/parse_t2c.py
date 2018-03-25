from __future__ import division, print_function, unicode_literals
__copyright__ = 'Copyright (C) Volker Diels-Grabsch <v@njh.eu>'

from .parse_records import parse_records
from datetime import date
from datetime import datetime
from re import split

def find_alternative_field_name(record_dict, field_name):
    for i in xrange(2, 100):
        alternative_field_name = '{field_name}_{i}'.format(**locals())
        if alternative_field_name not in record_dict:
            return alternative_field_name
    raise ValueError('Unable to find alternative field name')

def parse_record_dict(record):
    record_dict = {}
    for field in record:
        field_name = field['field_name']
        value = {
            'first_line': field['first_line'],
            'additional_lines': field['additional_lines'],
        }
        if field_name in record_dict:
            alternative_field_name = find_alternative_field_name(record_dict, field_name)
            record_dict[alternative_field_name] = value
        else:
            record_dict[field_name] = value
    return record_dict

def parse_event_date(value):
    text = ' '.join([value['first_line']] + value['additional_lines'])
    try:
        start = datetime.strptime(text[:len('yyyy-mm-dd')], '%Y-%m-%d').date()
    except ValueError:
        start = date(1970, 1, 1)
    return {
        'start': start,
        'text': text,
    }

def parse_event_mott(value):
    return ' '.join([value['first_line']] + value['additional_lines'])

def parse_event_tags(value):
    return set(
        tag
        for line in [value['first_line']] + value['additional_lines']
        for tag in split(r' +', line)
        if tag != ''
    )

def parse_event_titl(value):
    return [value['first_line']] + value['additional_lines']

def parse_event(record):
    record_dict = parse_record_dict(record)
    field_parsers = [
        parse_event_date,
        parse_event_mott,
        parse_event_tags,
        parse_event_titl,
    ]
    empty_value = {
        'first_line': '',
        'additional_lines': [],
    }
    recognized_fields = {
        field_name: field_parser(record_dict.get(field_name, empty_value))
        for field_parser in field_parsers
        for field_name in [field_parser.func_name.decode('ascii')[len('parse_event_'):]]
    }
    unrecognized_fields = sorted(
        {
            'field_name': field_name,
            'first_line': value['first_line'],
            'additional_lines': value['additional_lines'],
        }
        for field_name, value in record_dict.iteritems()
        if field_name not in recognized_fields
    )
    event = recognized_fields
    event['unrecognized'] = unrecognized_fields
    return event

def parse_events(fileobj):
    for record in parse_records(fileobj):
        yield parse_event(record)

def sort_key_event(event):
    return (
        event['date'],
        event['titl'],
    )

def parse_sorted_events(fileobj):
    return sorted(parse_events(fileobj), key=sort_key_event)

def parse_t2c(fileobj):
    return parse_sorted_events(fileobj)
