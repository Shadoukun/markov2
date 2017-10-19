from functools import wraps

from .config import config


def is_admin(func):

    def wrapper(*args, **kwargs):
        if args[2] in config.admins:
            return func(*args, **kwargs)
        else:
            return

    return wrapper