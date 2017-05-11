from datetime import datetime
import random
import sys
import time
from enum import Enum
from uuid import uuid4

data = {}
JOURNAL = 'xtl_log.txt'

class Event(Enum):
    create = 'CREATE'

commands = {
    'add': Event.create
    }

def puid():
    return '%08x' % random.randrange(16 ** 8)


def emit_event(evt_type, data):
    timestamp = int(time.time())
    with open(JOURNAL, 'a') as f:
        f.write(f'{timestamp} {evt_type.value} {puid()} {data}\n')


def parse_cmd(args):
    cmd, rem = args[0], ' '.join(args[1:])
    emit_event(commands[cmd], rem)

if __name__ == '__main__':
    parse_cmd(sys.argv[1:])
