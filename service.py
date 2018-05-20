# inherit services from this class
class service:
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

    # override to show user's id not in standart way
    @staticmethod
    def get_id(id):
        return id

    # don't override
    @staticmethod
    def handle_message(user, msg):
        user.get_action(msg).handle()

services = []
