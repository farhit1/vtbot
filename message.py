from user_base import users
import datetime


class incorrect(Exception):
    def __init__(self, comment='incorrect command'):
        self.comment = comment


class message:
    def __init__(self, text, sender=None, receiver=None, attachments=None):
        self.sender = sender
        self.receiver = receiver
        self.text = text
        self.attachments = attachments

    def send(self):
        self.sent = True
        self.receiver.notify(self)

    def __repr__(self):
        if self.sender is None:
            return self.text
        return 'Message from %s%s:\n%s' % (
            self.sender.login,
            ' (%s)' % self.sender.get_service_login() if self.sender.show_service_name else '',
            self.text
        )


outbox = dict()

def flush_outbox():
    for (time, msg) in list(outbox.items()):
        if time < datetime.datetime.now():
            if not msg.receiver.mute:
                msg.send()
            del outbox[time]
