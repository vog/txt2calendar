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

TEvent = namedtuple('Event', 'start, end, summary, labeled_uris, description')

_LabeledUri = namedtuple('LabeledUri', 'uri, label')

def LabeledUri(uri, label):
    assert isinstance(uri, str)
    assert isinstance(label, str)
    return _LabeledUri(uri=uri, label=label)

EventList = namedtuple('EventList', 'events')

#def SingleDayEvent(start, summary, labeled_uris, description): # temp
def SingleDayEvent(start, summary, description):
    labeled_uris = [] # temp
    assert isinstance(start, datetime)
    assert isinstance(summary, str)
    assert isinstance(labeled_uris, list)
    assert isinstance(description, str)
    return TEvent(
        start=start,
        end=start + timedelta(days=1),
        summary=summary,
        labeled_uris=labeled_uris,
        description=description,
    )

def Kwargs(cls, *items):
    return Group(And(items)).setParseAction(lambda toks: cls(**toks[0].asDict()))

uri = Regex('https?://[A-Za-z0-9./-]+')

labeled_uri = Kwargs(
    LabeledUri,
    uri.setResultsName('uri'),
    Combine(Optional(QuotedString('"'))).setResultsName('label'),
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
    ]).setResultsName('summary'),
    #Group(ZeroOrMore(labeled_uri)).setResultsName('labeled_uris'), # temp
    MatchFirst([
        SkipTo(Literal(b'\n\n')),
        SkipTo(And([
            Literal(b'\n'),
            StringEnd(),
        ])),
    ]).setResultsName('description'),
)

events = Kwargs(
    EventList,
    OneOrMore(event).setResultsName('events'),
)

def generate_ical(filepath, event_list):
    stderr.write('Writing {filepath}\n'.format(**locals()))
    cal = Calendar()
    for event in event_list.events:
        cal_event = Event()
        cal_event.add('dtstart', event.start)
        cal_event.add('dtend', event.start + timedelta(days=1))
        cal_event.add('summary', event.summary)
        cal_event.add('description', event.description)
        cal.add_component(cal_event)
    ical_bytes = cal.to_ical()
    with open(filepath, 'wb') as f:
        f.write(ical_bytes)

def usage():
    stderr.write('Usage: txt2calendar DATA.txt\n')

def main():
    if len(argv) != 2:
        usage()
        return
    filename = argv[1]
    e = events.parseFile(filename, parseAll=True)[0]
    generate_ical('txt2cal.ics', e)

if __name__ == '__main__':
    main()
