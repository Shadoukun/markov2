import logging
import random

from markov.base import BaseClient
from markov.db import Database
from markov.config import config
from markov.model import Modeller


class Markov(BaseClient):

    def __init__(self):
        super().__init__()

        self.chattiness = 0.2

        self.db = Database()
        self.modeller = Modeller(self.db)

        self.connect(config.host, config.port)

    def on_connect(self, *args):
        for channel in config.channels:
            self.bot.join(channel)

    def on_kick(self, channel, target, by, reason=None):
        # rejoin channel if kicked.
        self.join(channel)

    def on_message(self, source, target, message):

        rand = random.random()
        if rand < self.chattiness:
            msg = self.modeller.generate_message(message)
            self.message(source, msg)

        # self.db.log(target, source, message)

    def on_mention(self, source, target, message):
            msg = self.modeller.generate_message(message)
            self.message(source, msg)

def run():
    bot = Markov()
    bot.bot.handle_forever()


if __name__ == '__main__':
    run()