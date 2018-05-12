class service:
    @staticmethod
    def handle_message(user, msg):
        user.get_action(msg).handle()

    # override
    @classmethod
    def launch(cls):
        raise Exception('set up %s.launch()' % cls.__name__)

    # override
    @classmethod
    def send_message(cls):
        raise Exception('set up %s.send_message(id, message)' % cls.__name__)

    # override
    @classmethod
    def handle(cls):
        raise Exception('set up %s.handle()' % cls.__name__)


services = []
