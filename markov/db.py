import mongoengine
import markovify
from collections import namedtuple
import string
import re

from .config import config


class Message(mongoengine.Document):
    user = mongoengine.StringField(required=True, max_length=200)
    host = mongoengine.StringField(required=True)
    channel = mongoengine.StringField(required=True)

    message = mongoengine.StringField(required=True)


class Database:

    def __init__(self):

        self.config = config
        mongoengine.connect('bot', host=config.dbhost, port=config.dbport)

    def get(self, username=None):

        messages = []

        if username:
            if isinstance(username, list):
                for name in username:
                    msgs = [m for m in Message.objects(user=name)]
                    messages = messages + msgs

            elif isinstance(username, str):
                messages = Message.objects(user=username)

        else:
            messages = Message.objects()

        return messages

    def log(self, nick, host, channel, message):

        if self._messageCheck(message):
            message = message.translate(string.punctuation)
            msg = Message(nick, host, channel, message)
            msg.save()

    def _messageCheck(self, message):

        exps = [

            re.compile(r"\<.*\>"), # anything in brackets. usually IRC nicks. <markov>
            re.compile(r'http(s|)\:.*\.'), # URLS
            re.compile(r"\d\d\:\d\d\:\d\d"), # Timestamps. 00:00:00
            re.compile(r"[/\\\s]?.*(?=.*[/\\])\w(/|\\|)"), # UNIX files paths and relative MS paths.
            re.compile(r'\w\:\\'), # Absolute windows filepaths.
            re.compile(r"\[.*\]") # Things in [] brackets.
        ]

        if len(message.split()) < 3:
            return False

        for exp in exps:
            if re.match(exp, message):
                return False

        return True


def main():

    db = Database()
    test = db.get()
    print(len(test))

if __name__ == '__main__':
    main()