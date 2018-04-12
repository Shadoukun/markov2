from markov.plugin import command, Plugin
from markov.decorators import is_admin
import inspect

class Chattiness(Plugin):
    '''Chattiness Command'''

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @is_admin
    @command(name="chattiness")
    def set_chattiness(self, source, target, message):
        old_chattiness = self.bot.chattiness
        self.bot.chattiness = float(message)

        self.bot.message(source, f'Chattiness changed from {old_chattiness} to {self.bot.chattiness}')