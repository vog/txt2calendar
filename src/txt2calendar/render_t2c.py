from __future__ import division, print_function, unicode_literals
__copyright__ = 'Copyright (C) Volker Diels-Grabsch <v@njh.eu>'

from .render_records import render_records

def render_event_date(event_date):
    return [event_date['text']]

def render_event_mott(event_mott):
    if event_mott == '':
        return None
    return [event_mott]

def render_event_tags(event_tags):
    if len(event_tags) == 0:
        return []
    return [' '.join(sorted(event_tags))]

def render_event_titl(event_titl):
    return event_titl

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
            'value_lines': field_renderer(event[field_name]),
        }
        for field_renderer in field_renderers
        for field_name in [field_renderer.func_name.decode('ascii')[len('render_event_'):]]
        for value_lines in [field_renderer(event[field_name])]
        if value_lines is not None
    ]
    unrecognized_fields = sorted(
        field
        for field in event['unrecognized']
    )
    record = recognized_fields + unrecognized_fields
    return record

def render_events(events):
    for event in events:
        yield render_event(event)

def render_t2c(fileobj, events):
    records = render_events(events)
    return render_records(fileobj, records)
