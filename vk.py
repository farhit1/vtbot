from service import *
from user import user
from message import message
import urllib.request
import json
import urllib.parse


class vk(service):
    server = HIDDEN
    key = HIDDEN

    access_token = HIDDEN

    users = {}
    timestamp = 1

    @staticmethod
    def send_message(id, message):
        send_url = 'https://api.vk.com/method/messages.send?user_id=%s&message=%s&access_token=%s&v=5.50' % (
            id, urllib.parse.quote(str(message), safe=''), vk.access_token,
        )
        with urllib.request.urlopen(send_url) as url:
            print(json.loads(url.read().decode()))

    @staticmethod
    def long_poll_url():
        return '%s?act=a_check&key=%s&ts=%s' % (
            vk.server, vk.key, vk.timestamp
        )

    @staticmethod
    def handle():
        with urllib.request.urlopen(vk.long_poll_url()) as url:
            data = json.loads(url.read().decode())
            for action in data['updates']:
                if action['type'] == 'message_new':
                    text = action['object']['body']
                    uid = str(action['object']['user_id'])
                    if uid not in vk.users:
                        text = '/start'
                        vk.users[uid] = user(vk, uid, uid)
                    service.handle_message(vk.users[uid], message(text))
            vk.timestamp = str(max(int(vk.timestamp), int(data['ts'])))

    @staticmethod
    def launch():
        with urllib.request.urlopen(vk.long_poll_url()) as url:
            data = json.loads(url.read().decode())
            vk.timestamp = data['ts']

services.append(vk)
