from markov.plugin import command, Plugin
from markov.decorators import is_admin

class Chattiness(Plugin):
    '''Chattiness Command'''

    def __init__(self):
        self.bot = None

    @command(name="chattiness")
    @is_admin
    def set_chattiness(self, source, target, message):
        old_chattiness = self.bot.chattiness
        self.bot.chattiness = float(message)

        self.bot.message(source, f'Chattiness changed from {old_chattiness} to {self.bot.chattiness}')