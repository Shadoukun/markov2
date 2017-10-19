import inspect
from pprint import pprint
from functools import partial

class Plugin:
    ''' Base class for plugins.
        Automatically populates Plugin.plugins
        with list of subclasses.
    '''

    plugins = []
    ignore = ['name', 'callback', 'commands']

    def __init__(self):
        self.commands = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        plugin = cls()
        plugin.commands = []

        # Add commands to plugin's list of commands.
        for _, var in vars(cls).items():
            if type(var).__name__ == 'Command':
                cmd = var

                # Add plugin attributes to command.
                for name, attr in vars(plugin).items():

                    # skip variables we dont want
                    if name not in Plugin.ignore:
                        cmd.__dict__[name] = attr

                plugin.commands.append(cmd)

        Plugin.plugins.append(plugin)


class Command:
    '''Empty command Class'''

    def __init__(self, name=None, callback=None):
        self.name = name
        self.callback = callback


def command(name, **attrs):

    def decorator(f):
        return Command(name, f)

    return decorator