from __future__ import division, print_function, unicode_literals
__copyright__ = 'Copyright (C) Volker Diels-Grabsch <v@njh.eu>'

from .render_t2c import render_t2c
from datetime import date
from io import BytesIO

def test_render_t2c():
    events = [
        {
            'titl': [
                '@FreeCodeCamp Meetup',
                'fdfdofd',
                'fddf',
            ],
            'mott': 'learn to code for free!',
            'date': {
                'start': date(2017, 11, 16),
                'text': '2017-11-16 10-17',
            },
            'tags': set(),
            'unrecognized': [
                {
                    'field_name': 'mott_2',
                    'first_line': 'learn to code for free!',
                    'additional_lines': [],
                },
            ],
        },
        {
            'titl': [
                '@FreeCodeCamp Meetup',
                'fdfdofd',
                'fddf',
            ],
            'mott': '',
            'date': {
                'start': date(2017, 11, 17),
                'text': '2017-11-17 10-17',
            },
            'tags': set([
                '#CSS3',
                '#FreeCodeCamp',
                '#HTML5',
                '#JavaScript',
                '#Private',
            ]),
            'unrecognized': [
                {
                    'field_name': 'home',
                    'first_line': 'https://www.meetup.com/FreeCodeCamp-Berlin/events/245113121',
                    'additional_lines': [],
                },
                {
                    'field_name': 'host',
                    'first_line': '@BodoEichstaedt',
                    'additional_lines': [],
                },
                {
                    'field_name': 'link',
                    'first_line': 'https://github.com/FreeCodeCamp http://example.com/FreeCodeCamp2',
                    'additional_lines': [],
                },
                {
                    'field_name': 'venu',
                    'first_line': '@INBerlinev Lehrter Str 53, 10557 Berlin http://www.in-berlin.de/space/',
                    'additional_lines': [],
                },
            ],
        },
    ]
    t2c_bytes = (
        b'titl: @FreeCodeCamp Meetup\n'
        b' fdfdofd\n'
        b' fddf\n'
        b'mott: learn to code for free!\n'
        b'date: 2017-11-16 10-17\n'
        b'tags:\n'
        b'mott_2: learn to code for free!\n'
        b'\n'
        b'titl: @FreeCodeCamp Meetup\n'
        b' fdfdofd\n'
        b' fddf\n'
        b'date: 2017-11-17 10-17\n'
        b'tags: #CSS3 #FreeCodeCamp #HTML5 #JavaScript #Private\n'
        b'home: https://www.meetup.com/FreeCodeCamp-Berlin/events/245113121\n'
        b'host: @BodoEichstaedt\n'
        b'link: https://github.com/FreeCodeCamp http://example.com/FreeCodeCamp2\n'
        b'venu: @INBerlinev Lehrter Str 53, 10557 Berlin http://www.in-berlin.de/space/\n'
    )
    f = BytesIO()
    render_t2c(f, events)
    assert t2c_bytes == f.getvalue()
