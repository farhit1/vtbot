class command:
    def __init__(self, alias, action, comment, is_shown=(lambda user: True)):
        self.alias = alias
        self.execute = action
        self.comment = comment
        self.is_shown = is_shown
