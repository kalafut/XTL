from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.completion import Completer, Completion

history = InMemoryHistory()
html_completer = WordCompleter(['<html>', '<body>', '<head>', '<title>'])

tasks = []

class MyCustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        yield Completion('completion', start_position=-1)

def handle_line(line):
    cmd, rem = line.split(maxsplit=1)
    if cmd == 'task':
        tasks.append(rem)
    elif cmd == 'list':
        for t in tasks:
            print(t)


if __name__ == '__main__':
    #parse_cmd(sys.argv[1:])
    while True:
        text = prompt('> ', history=history, vi_mode=True, completer=MyCustomCompleter())
        handle_line(text)
        print('You said: %s' % text)
