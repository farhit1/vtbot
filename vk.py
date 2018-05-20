from service import *
from user import user
from message import message
import urllib.request
import json
import urllib.parse
import time
import sys

class vk(service):
    longpoll_server = HIDDEN
    access_token = HIDDEN
    api_version = HIDDEN
    group_id = HIDDEN

    longpoll_key = None
    users = {}
    ts = 1

    @staticmethod
    def build_url(method, properties=dict()):
        properties['access_token'] = vk.access_token
        properties['v'] = vk.api_version
        return 'https://api.vk.com/method/%s?%s' % (
            method,
            urllib.parse.urlencode(properties)
        )

    @staticmethod
    def send_message(id, message):
        with urllib.request.urlopen(vk.build_url('messages.send', {
            'user_id': id,
            'message': message
        })) as url:
            pass

    @staticmethod
    def long_poll_url():
        return '%s?%s' % (
            vk.longpoll_server, urllib.parse.urlencode({
                'act': 'a_check',
                'key': vk.key,
                'ts': vk.ts
            })
        )

    @staticmethod
    def handle():
        try:
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
                vk.ts = data['ts']
        except:
            vk.launch()

    @staticmethod
    def launch():
        while (True):
            try:
                with urllib.request.urlopen(vk.build_url('groups.getLongPollServer', {
                    'group_id': vk.group_id
                })) as url:
                    data = json.loads(url.read().decode())
                    vk.key = data['response']['key']
                with urllib.request.urlopen(vk.long_poll_url()) as url:
                    data = json.loads(url.read().decode())
                    vk.ts = data['ts']
                return
            except:
                print('vk.launch() failed, retry', end='', file=sys.stderr)
                time.sleep(5)
                pass

    @staticmethod
    def get_id(id):
        return 'id%s' % id.split('@')[1]

services.append(vk)
