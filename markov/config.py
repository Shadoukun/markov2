import yaml
import logging
import logging.config

CONFIG = './config.yaml'


class Config:

    _instance = None
    # Singleton
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

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
