from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    @property
    def role(self):
        if self.id == 'anamicusoftwire':
            return 'writer'

        return 'reader'