from __future__ import division, print_function, unicode_literals
__copyright__ = 'Copyright (C) Volker Diels-Grabsch <v@njh.eu>'

from .render_records import render_records

def render_event_date(event_date):
    return {
        'first_line': event_date['text'],
        'additional_lines': [],
    }

def render_event_mott(event_mott):
    if event_mott == '':
        return None
    return {
        'first_line': event_mott,
        'additional_lines': [],
    }

def render_event_tags(event_tags):
    return {
        'first_line': ' '.join(sorted(event_tags)),
        'additional_lines': [],
    }

def render_event_titl(event_titl):
    return {
        'first_line': event_titl[0],
        'additional_lines': event_titl[1:],
    }

def render_event(event):
    field_renderers = [
        render_event_titl,
        render_event_mott,
        render_event_date,
        render_event_tags,
    ]
    recognized_fields = [
        {
            'field_name': field_name,
            'first_line': renderer_result['first_line'],
            'additional_lines': renderer_result['additional_lines'],
        }
        for field_renderer in field_renderers
        for field_name in [field_renderer.func_name.decode('ascii')[len('render_event_'):]]
        for renderer_result in [field_renderer(event[field_name])]
        if renderer_result is not None
    ]
    unrecognized_fields = sorted(event['unrecognized'], key=lambda field: field['field_name'])
    record = recognized_fields + unrecognized_fields
    return record

def render_events(events):
    for event in events:
        yield render_event(event)

def render_t2c(fileobj, events):
    records = render_events(events)
    return render_records(fileobj, records)
