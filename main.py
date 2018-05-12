import service
import message
import sys

import telegram
import vk


def eprint(msg):
    print(msg, end='', file=sys.stderr)


if __name__ == '__main__':
    for s in service.services:
        eprint(s.__name__)
        s.launch()
        eprint(' launched\n')
    eprint('Listening...\n')

    while (True):
        # some services are not launched asynchronously
        for s in service.services:
            s.handle()
        # deliver sent messages
        message.flush_outbox()
