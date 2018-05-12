import datetime
from message import *
from user_base import *
import contextlib
from command import command


# inherit query from this class
class query:
    # override
    desc = 'No information provided'
    # override
    back = None

    # override if this query
    # can use not only commands
    def handler(self):
        raise incorrect()
    # override to show small_info
    small_info_show = False

    def __init__(self, user, message):
        self.user = user
        self.message = message

    def set_back(self):
        self.user.next_action(self.back)

    def info(self):
        self.user.notify(message(
            "%s\n\nAvailable commands:\n%s\n\n" % (
                self.desc,
                '\n'.join(
                    map(lambda command: "%s - %s" % (
                        command.alias,
                        command.comment
                    ), (
                        command for command in self.commands
                        if (command.comment and command.is_shown(self.user))
                    ))
                )
            )
        ))

    def small_info(self):
        self.user.notify(message(
            "%s\n\n/info - available commands" % self.desc
        ))

    def about(self):
        msg = """
VTBot - send and receive messages from anywhere. \
We erase the boundaries between social networks.\n\n\
Telegram: t.me/vtbot_bot\n\
VK: vk.com/vtbot\n\
GitHub: github.com/farhit1/vtbot
        """
        self.user.notify(message(msg))

    commands = [
        command('/back', set_back, 'go back',
                lambda user: user.action.back is not user.action),
        command('/info', info, ''),
        command('/start', small_info, ''),
        command('/about', about, 'about this bot')
    ]

    def handle(self):
        try:
            msg = self.message.text
            for command in self.commands:
                if command.is_shown(self.user) and msg == command.alias:
                    exec('self.%s()' % command.execute.__name__)
                    return
            self.handler()
        except incorrect as e:
            self.user.notify(message('Error: %s' % e.comment))


class register(query):
    desc = 'Registration in VTBot.\nType your nickname.'
    small_info_show = True

    def handler(self):
        username = self.message.text
        if not check_username(username):
            raise incorrect("""
username should be a string, containing at least 4 letters
            """)
        if username in users:
            raise incorrect('username is already taken')
        users[username] = self.user
        users_by_service_login[self.user.get_service_login()] = self.user
        self.user.login = username
        self.user.next_action(start)

register.back = register


class start(query):
    desc = 'Main menu.'

    def start_handle(self):
        self.user.mute = False
        self.user.notify(message('Mute mode is off'))

    def stop_handle(self):
        self.user.mute = True
        self.user.notify(message('Mute mode is on'))

    def send_handle(self):
        self.user.next_action(send_message.get_receiver)

    def my_name(self):
        message_text = 'Your nickname is %s\n' % self.user.login
        if self.user.show_service_name:
            message_text += ('You can also be found by %s' %
                             self.user.get_service_login())
        self.user.notify(message(message_text))

    def hide_id(self):
        self.user.show_service_name = False
        self.user.notify(message("""
Your service id was hidden. Your messages' receivers would not see \
your service id. You couldn't be found by your service id.
        """))

    def disclose_id(self):
        self.user.show_service_name = True
        self.user.notify(message('Your service nickname was disclosed.'))

    commands = list(query.commands)
    commands.append(command('/continue', start_handle,
                            'continue receiving messages',
                            lambda user: user.mute))
    commands.append(command('/pause', stop_handle, 'pause receiving messages',
                            lambda user: not user.mute))
    commands.append(command('/send', send_handle, 'send a message'))
    commands.append(command('/name', my_name, 'your nickname'))
    commands.append(command('/hide', hide_id, 'hide service id',
                            lambda user: user.show_service_name))
    commands.append(command('/unhide', disclose_id,
                            'disclose service id',
                            lambda user: not user.show_service_name))

start.back = start


class send_message:
    class get_receiver(query):
        desc = "Type receiver's nickname."
        small_info_show = True

        def handler(self):
            username = self.message.text
            receiver = None
            if username in users:
                receiver = users[username]
            if (username in users_by_service_login and
                    users_by_service_login[username].show_service_name):
                receiver = users_by_service_login[username]
            if receiver is None:
                raise incorrect('no such user')
            self.user.bucket['send_message_to'] = receiver
            self.user.next_action(send_message.get_time)

    class get_time(query):
        desc = """
Type after how many minutes message would be sent.\n
Type 0 to send it immediately.\
        """
        small_info_show = True

        def handler(self):
            time = self.message.text
            if not time.isdigit() or int(time) < 0:
                raise incorrect('expected non-negative integer')
            self.user.bucket['send_message_delay'] = int(time)
            self.user.next_action(send_message.get_message)

    class get_message(query):
        desc = 'Type message.'
        small_info_show = True

        def handler(self):
            time = (
                datetime.datetime.now() +
                datetime.timedelta(
                    minutes=self.user.bucket['send_message_delay']
                )
            )
            outbox[time] = message(
                self.message.text,
                users[self.user.login],
                self.user.bucket['send_message_to'],
                self.message.attachments
            )
            self.user.notify(message('Sent!'))
            self.user.next_action(start)

send_message.get_receiver.back = start
send_message.get_time.back = send_message.get_receiver
send_message.get_message.back = send_message.get_time
