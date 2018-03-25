from __future__ import division, print_function, unicode_literals
__copyright__ = 'Copyright (C) Volker Diels-Grabsch <v@njh.eu>'

from datetime import datetime
from datetime import timedelta

def in_filter(event):
    min_start_date = datetime.now().date() - timedelta(weeks=2) 
    return all([
        '#Private' not in event['tags'],
        '#FLOSS' in event['tags'],
        event['date']['start'] >= min_start_date,
    ])

def filter_events(events):
    for event in events:
        if in_filter(event):
            yield event
