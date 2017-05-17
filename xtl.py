from collections import namedtuple
from datetime import datetime
import random
import re
import sys
import time
from enum import Enum
from uuid import uuid4

data = {}
JOURNAL = 'xtl_log.txt'

class Command(Enum):
    create = 'CREATE'
    link = 'LINK'

class Event:
    def __init__(self):
        self.uid = puid()
        self.timestamp = int(time.time())

    def encode(self):
        return f'{self.timestamp} {self.encode_command()} {self.uid}'

class Create(Event):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def encode_command(self):
        return f'CREATE {self.data}'

commands = {
    'add': Create
    }


Object = namedtuple('Object', 'uid timestamp data')
Link = namedtuple('Link', 'uid timestamp a_uid b_uid')

class State:
    def __init__(self):
        self._init_patterns()
        self._objects = {}
        self._links = {}
        self._aliases = {}

        with open(JOURNAL) as self.f:
            self._parse_file()
        self.f = open(JOURNAL, 'a')

    def _init_patterns(self):
        self.journal_pats = [
            (re.compile(r'(?P<timestamp>\d+) +LINK +(?P<uid>[0-9a-f]+) +(?P<a_uid>[0-9a-f]+) +(?P<b_uid>[0-9a-f]+) *$'), self._journal_link),
            (re.compile(r'(?P<timestamp>\d+) +CREATE +(?P<uid>[0-9a-f]+) +(?P<data>.*?) *$'), self._journal_add_object),
            (re.compile(r'(?P<timestamp>\d+) +ALIAS +(?P<uid>[0-9a-f]+) +(?P<data>.*?) *$'), self._journal_alias),
            ]

    def _add_object(self, o):
        if o.uid in self._objects:
            raise Exception(f'Object {o.uid} already exists')
        self._objects[o.uid] = o

    def _add_link(self, o):
        if o.uid in self._links:
            raise Exception(f'Link {o.uid} already exists')
        for uid in [o.a_uid, o.b_uid]:
            if uid not in self._objects:
                raise Exception(f'Link reference {uid} not found')
        self._links[o.uid] = o

    def _journal_add_object(self, vals):
        self._add_object(Object(**vals))

    def _journal_link(self, vals):
        self._add_link(Link(**vals))

    #def _journal_alias(self, vals):
    #    if
    #    self._add_link(Link(**vals))

    def _parse_file(self):
        for line in self.f:
            matched = False
            for pat, fn in self.journal_pats:
                match = pat.match(line)
                if match:
                    matched = True
                    d = match.groupdict()
                    d['timestamp'] = int(d['timestamp'])
                    fn(d)
                    continue
            if not matched:
                raise Exception(f'Couldn\'t parse line: {line}')

    def getall(self):
        return self._objects.values()

    def get(self):
        return self._objects.values()

    def links_to(self, src_uid, tgt_uid):
        for link in self._links.values():
            if link.a_uid == src_uid and link.b_uid == tgt_uid:
                return True
        return False

    @property
    def q(self):
        return Query(iter(self.getall()), self)


class Query:
    def __init__(self, start, state):
        self._results = start
        self._state = state

    def __iter__(self):
        return self._results

    def linked(self, uid):
        return Query((x for x in self._results if self._state.links_to(x.uid, uid)), self._state)

    def search(self, term):
        return Query((x for x in self._results if term.casefold() in x.data.casefold()), self._state)


def puid():
    return '%08x' % random.randrange(16 ** 8)


def emit_event(evt_type, data):
    cmd = evt_type(data)
    with open(JOURNAL, 'a') as f:
        f.write(f'{cmd.encode()}\n')


def parse_cmd(args):
    cmd, rem = args[0], ' '.join(args[1:])
    emit_event(commands[cmd], rem)


def todo_list(s: State):
    todos = s.q.linked('Tasks')
    for t in todos:
        print(t.data)

if __name__ == '__main__':
    s = State()
    todo_list(s)
    #parse_cmd(sys.argv[1:])
