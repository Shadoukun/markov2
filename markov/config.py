import yaml
import logging
import logging.config

class Singleton(type):

    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(cls, bases, dict)
        cls._instanceDict = {}

    def __call__(cls, *args, **kwargs):
        argdict = {'args': args}
        argdict.update(kwargs)
        argset = frozenset(argdict)
        if argset not in cls._instanceDict:
            cls._instanceDict[argset] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instanceDict[argset]


class Config(metaclass=Singleton):

    def __init__(self):
        self.loadConfig('config.yaml')
        self.setup_logging()

    def loadConfig(self, config):
        with open(config, 'r') as stream:
            data = yaml.load(stream)

            for k, v in data.items():
                self.__dict__[k] = v

    def setup_logging(self):
        logconfig = self.logging

        if logconfig:
            logging.config.dictConfig(logconfig)

        else:
            logging.basicConfig(level=INFO)

        logger = logging.getLogger(__name__)

config = Config()

if __name__ == '__main__':
    test = Config()
    test2 = Config()
    print(test)
    print(test2)