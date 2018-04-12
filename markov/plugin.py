import inspect
from pprint import pprint
from functools import partial, wraps

class PluginHandler:

    plugins = []

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PluginHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self, bot):
        self.bot = bot

class Plugin:

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PluginHandler.plugins.append(cls)

    def __init__(self):
        self.commands = []

        for i in dir(self):
            i = getattr(self, i)
            if isinstance(i, Command):
                self.commands.append(i)

class Command:
    '''Empty command Class'''

    def __init__(self, name=None, callback=None):
        self.name = name
        self.callback = callback

def command(name, **attrs):

    def decorator(f):
        cmd = Command(name, f)
        return Command(name, f)

    return decorator
