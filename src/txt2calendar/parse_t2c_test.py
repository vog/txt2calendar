from __future__ import division, print_function, unicode_literals
__copyright__ = 'Copyright (C) Volker Diels-Grabsch <v@njh.eu>'

from .parse_t2c import parse_t2c
from datetime import date
from io import BytesIO

def test_parse_t2c():
    t2c = BytesIO(
        b'\n'
        b'titl: @FreeCodeCamp Meetup\n'
        b' fdfdofd\n'
        b' fddf\n'
        b'date: 2017-11-17 10-17\n'
        b'home: https://www.meetup.com/FreeCodeCamp-Berlin/events/245113121\n'
        b'venu: @INBerlinev Lehrter Str 53, 10557 Berlin http://www.in-berlin.de/space/\n'
        b'tags: #Private #FreeCodeCamp #HTML5 #CSS3 #JavaScript \n'
        b'link: https://github.com/FreeCodeCamp http://example.com/FreeCodeCamp2\n'
        b'host: @BodoEichstaedt\n'
        b'\n'
        b'\n'
        b'titl: @FreeCodeCamp Meetup\n'
        b' fdfdofd\n'
        b' fddf\n'
        b'mott: learn to code for free!\n'
        b'mott: learn to code for free!\n'
        b'date: 2017-11-16 10-17\n'
        b'\n'
    )
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
    assert events == parse_t2c(t2c)
