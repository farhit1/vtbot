import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from service import *
from user import user
from message import message


class telegram(service):
    TOKEN = HIDDEN
    users = {}

    @staticmethod
    def on_message(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if chat_id not in telegram.users:
            telegram.users[chat_id] = user(telegram, chat_id,
                                           msg['chat']['username'])
        service.handle_message(telegram.users[chat_id], message(msg['text']))

    # button click
    @staticmethod
    def on_callback(msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        service.handle_message(telegram.users[from_id], message(msg['data']))

    @staticmethod
    def get_keyboard(text):
        keyboard = []
        for line in text.split('\n'):
            if len(line) > 0 and line[0] == '/':
                command, description = line.split(' - ')
                keyboard.append([InlineKeyboardButton(
                    text=description.capitalize(),
                    callback_data=command)]
                )
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @staticmethod
    def send_message(id, message):
        telegram.bot.sendMessage(
            id, str(message),
            reply_markup=telegram.get_keyboard(message.text)
        )

    @staticmethod
    def launch():
        telegram.bot = telepot.Bot(telegram.TOKEN)
        telegram.bot.message_loop({
                'chat': telegram.on_message,
                'callback_query': telegram.on_callback
        })

    @staticmethod
    def handle():
        pass

services.append(telegram)
