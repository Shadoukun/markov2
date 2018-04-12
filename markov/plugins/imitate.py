from markov.plugin import command, Plugin
from markov.decorators import is_admin


class Imitate(Plugin):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.imitating = False

    @is_admin
    @command(name="imitate")
    def set_imitate(self, source, target, message):

        message = message.strip()

        if message == 'off':

            if not self.imitating:
                return

            self.bot.modeller.thread.cancel()
            self.bot.modeller.get_model()
            self.bot.message(source, "imitation: Off")

            self.imitating = False

        else:

            text = self.bot.modeller.get_text(message)

            if text:
                self.bot.modeller.thread.cancel()
                self.bot.modeller.get_model(text, repeat=False)
                self.bot.message(source, f"Imitating {message}")

                self.imitating = True

            else:
                self.bot.message(source, "idk who that is")
