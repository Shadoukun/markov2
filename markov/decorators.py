from .config import config
from functools import wraps
from .plugin import Command



def is_admin(func):
    original_callback = func.callback

    def wrapper(*args, **kwargs):
        print(args)
        if args[2] in config.admins:
            original_callback(*args, **kwargs)

    func.callback = wrapper
    return func