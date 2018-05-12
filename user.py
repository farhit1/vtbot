from query import *

users = {}

class user:
    def __init__(self, service, service_id, service_name):
        self.service = service
        self.service_id = service_id
        self.service_name = service_name
        self.login = None  # known when registration is complete
        self.action = register
        self.bucket = dict()
        self.mute = False
        self.show_service_name = True

    def get_action(self, message):
        return self.action(self, message)

    def notify(self, message):
        self.service.send_message(self.service_id, message)

    def next_action(self, action):
        self.action = action
        if self.action.small_info_show:
            self.get_action('').small_info()
        else:
            self.get_action('').info()

    def get_service_login(self):
        return '%s@%s' % (self.service.__name__, self.service_name)
