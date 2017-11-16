from __future__ import division, print_function, unicode_literals
__copyright__ = 'Copyright (C) Volker Diels-Grabsch <v@njh.eu>'

from collections import namedtuple
from datetime import datetime
from datetime import timedelta
from icalendar import Calendar
from icalendar import Event
from pyparsing import And
from pyparsing import Combine
from pyparsing import Empty
from pyparsing import Group
from pyparsing import LineEnd
from pyparsing import LineStart
from pyparsing import Literal
from pyparsing import MatchFirst
from pyparsing import OneOrMore
from pyparsing import Optional
from pyparsing import ParseResults
from pyparsing import QuotedString
from pyparsing import Regex
from pyparsing import SkipTo
from pyparsing import StringEnd
from pyparsing import White
from pyparsing import Word
from pyparsing import ZeroOrMore
from pyparsing import tokenMap
from pyparsing import ungroup
from sys import argv
from sys import stderr
from sys import stdin
from sys import stdout

TEvent = namedtuple('Event', 'start, end, summary, labeled_uris, description')

_LabeledUri = namedtuple('LabeledUri', 'uri, label')

def LabeledUri(uri, label):
    assert isinstance(uri, unicode)
    assert isinstance(label, unicode)
    return _LabeledUri(uri=uri, label=label)

_EventList = namedtuple('EventList', 'events')

def event_sort_key(event):
    return event.start, event.end, event.summary

def SortedEventList(events):
    return _EventList(
        events=sorted(events, key=event_sort_key),
    )

#def SingleDayEvent(start, summary, labeled_uris, description): # temp
def SingleDayEvent(start, summary, description):
    labeled_uris = [] # temp
    assert isinstance(start, datetime)
    assert isinstance(summary, unicode)
    assert isinstance(labeled_uris, list)
    assert isinstance(description, unicode)
    return TEvent(
        start=start,
        end=start + timedelta(days=1),
        summary=summary,
        labeled_uris=labeled_uris,
        description=description,
    )

def Kwargs(cls, *items):
    return Group(And(items)).setParseAction(lambda toks: cls(**toks[0].asDict()))

def decodeUtf8(b):
    return b.decode('utf-8')

uri = Regex('https?://[A-Za-z0-9./-]+')

labeled_uri = Kwargs(
    LabeledUri,
    uri.setParseAction(tokenMap(decodeUtf8)).setResultsName('uri'),
    Combine(Optional(QuotedString('"'))).setParseAction(tokenMap(decodeUtf8)).setResultsName('label'),
)

spaced_date = Kwargs(
    datetime,
    Regex('[0-9]{4}').setParseAction(tokenMap(int)).setResultsName('year'),
    Regex('[0-9]{2}').setParseAction(tokenMap(int)).setResultsName('month'),
    Regex('[0-9]{2}').setParseAction(tokenMap(int)).setResultsName('day'),
    Optional(Regex('[0-9]{2}')).suppress(),
    MatchFirst([
        Regex('[A-Z][a-z]{2}'),
        Regex('[A-Z][a-z]{1}'),
    ]).suppress(),
)

event = Kwargs(
    SingleDayEvent,
    spaced_date.setResultsName('start'),
    MatchFirst([
        And([
            Optional(Literal(b'???')).suppress(),
            Optional(Regex('[0-9h:-]+')).suppress(),
            Optional(Regex('@[^ \n]+')).suppress(), # location
            Optional(Regex('Day[0-9]/[0-9]')).suppress(),
            Optional(Regex('ALLDAY')).suppress(),
        ]),
        And([
            Optional(Regex('[^ \n]+')).suppress(), # location
            Optional(Regex('Day[0-9]/[0-9]')).suppress(),
            Optional(Regex('[0-9h:-]+')).suppress(),
        ]),
    ]),
    MatchFirst([
        QuotedString('"'),
        Regex('[^\n]+')
    ]).setParseAction(tokenMap(decodeUtf8)).setResultsName('summary'),
    #Group(ZeroOrMore(labeled_uri)).setResultsName('labeled_uris'), # temp
    MatchFirst([
        SkipTo(Literal(b'\n\n')),
        SkipTo(And([
            Literal(b'\n'),
            StringEnd(),
        ])),
    ]).setParseAction(tokenMap(decodeUtf8)).setResultsName('description'),
)

events = Kwargs(
    SortedEventList,
    OneOrMore(event).setResultsName('events'),
)

def parse(fileobj):
    return events.parseFile(fileobj, parseAll=True)[0]

def generate_ics(fileobj, event_list):
    cal = Calendar()
    for event in event_list.events:
        cal_event = Event()
        cal_event.add('dtstart', event.start)
        cal_event.add('dtend', event.start + timedelta(days=1))
        cal_event.add('summary', event.summary)
        cal_event.add('description', event.description)
        cal.add_component(cal_event)
    ical_bytes = cal.to_ical()
    fileobj.write(ical_bytes)

def datetime_format_24_00(d, is_end):
    if is_end and (d.hour, d.minute, d.second, d.microsecond) == (0, 0, 0, 0):
        return (d - timedelta(days=1)).strftime('%Y-%m-%d 24:00')
    return d.strftime('%Y-%m-%d %H:%M')

def generate_txt(fileobj, event_list):
    output = '\n'.join(
        (
            'from: {start}\n'
            'unto: {end}\n'
            'titl: {event.summary}\n'
            'rest:\n'
            '{rest}'
        ).format(
            start=datetime_format_24_00(event.start, is_end=False),
            end=datetime_format_24_00(event.end, is_end=True),
            rest=''.join(
                '    {description_line}\n'.format(**locals())
                for description_line in event.description.strip().split('\n')
            ),
            **locals()
        )
        for event in event_list.events
    )
    fileobj.write(output.encode('utf-8'))

def usage(generators):
    stderr.write(
        'txt2calendar 0.1\n'
        '\n'
        'Usage:\n'
        '\n'
        '    txt2calendar OUTPUT_FORMAT < INPUT_FILE > OUTPUT_FILE\n'
        '\n'
        'Input format:\n'
        '\n'
        '    recognized automatically\n'
        '\n'
        'Output formats:\n'
        '\n'
        '    ' + ', '.join(sorted(generators.iterkeys())) + '\n'
        '\n'
        'Example:\n'
        '\n'
        '    txt2calendar ics < input.txt > output.ics\n'
        '\n'
    )

def main():
    generators = {
        'ics': generate_ics,
        'txt': generate_txt,
    }
    if len(argv) != 2:
        return usage(generators)
    output_format = argv[1]
    try:
        generate = generators[output_format]
    except KeyError:
        return usage(generators)
    e = parse(stdin)
    generate(stdout, e)

if __name__ == '__main__':
    main()
