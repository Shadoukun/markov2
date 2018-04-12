import pydle
import re

from blinker import signal

from .config import config
from .plugin import *
from .plugins import *

import logging


class Event:
    '''Convenience class for blinker signal
       Automatically sends signal name as sender.'''

    def __init__(self, name):
        self.name = name

    def send(self, **kwargs):
        signal(self.name).send(self.name, **kwargs)


class Events:

    def __init__(self, bot):
        self.bot = bot

        self.events = [
            signal('on_connect'),
            signal('on_message'),
            signal('on_mention'),
            signal('on_command')
            ]

        self.register_events()

    def register_events(self):

        for e in self.events:
            if hasattr(self.bot, e.name):
                e.connect(self.process_event)

    def process_event(self, name, *args, **kwargs):
        if hasattr(self.bot, name):
            getattr(self.bot, name)(*args, **kwargs)


class IRCClient(pydle.Client):

    def __init__(self, config, **kwargs):
        super().__init__(config.nick, config.altnicks, config.username, config.realname, **kwargs)
        self.config = config


    def on_connect(self):
        Event("on_connect").send()

    def on_kick(self, channel, target, by, reason=None):
        Event("on_kick").send(channel=channel, target=target, by=by, reason=reason)

    def on_message(self, source, target, message):

        if self._mentioned(message):
            Event("on_mention").send(source=source, target=target, message=message)

        elif self._is_command(message):
            Event("on_command").send(source=source, target=target, message=message)

        else:
            Event("on_message").send(source=source, target=target, message=message)


    def _mentioned(self, message):
        ''' Check if bot was mentioned in message'''
        if re.match(f"^{self.nickname}", message):
            return True
        else:
            return False

    def _is_command(self, message):
        '''Test if a message begins with a command'''
        if message.startswith(config.commandchar):
            return True

    @property
    def logger(self):
        if not hasattr(self, "_logger"):
            self._logger = logging.getLogger(self.__class__.__name__)

        return self._logger

    @logger.setter
    def logger(self, value):
        pass

class BaseClient:
    '''Base client for IRC bot'''

    def __init__(self):
        self.bot = IRCClient(config)
        self.eventhandler = Events(self)
        self.pluginhandler = PluginHandler(self)

        self.plugins = []
        self.commands = []

        self.load_plugins()


    def load_plugins(self):
        ''' Load plugins from Plugin class'''

        for plugin in PluginHandler.plugins:
            plugin = plugin(self)

            # add commands from plugins
            for cmd in plugin.commands:
                # pass bot to the command
                cmd.bot = self

                self.commands.append(cmd)

            self.plugins.append(plugin)

    def process_commands(self, source, target, message):

        # try to split command and args
        try:
            cmd, args = message.split(" ", 1)

        except ValueError:
            cmd = message
            args = None

        # Check command in list of bot commands.
        try:
            for c in self.commands:
                if cmd == f"{config.commandchar}{c.name}":
                    c.callback(c, source, target, args)

        except Exception as e:
            self.logger.info(f"Command Failed.\n{command}\n{args}")
            self.logger.info(e)

    def connect(self, host, port, tls=False, tls_verify=False):
        self.bot.connect(host, port, tls=tls, tls_verify=tls_verify)

    def join(self, channel):
        self.bot.join(channel)

    def message(self, channel, message):
        self.bot.message(channel, message)

    ## Overrideable Methods ##

    def on_command(self, source, target, message):
        self.process_commands(source, target, message)

    def on_connect(self, *args):
        pass

    def on_message(self, source, target, message):
        pass

    def on_kick(self, channel, target, by, reason=None):
        pass

    def on_mention(self, source, target, message):
        pass


