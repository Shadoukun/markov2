import markovify
import threading
import logging
import random
import spacy
import re

from .config import config

nlp = spacy.load("en")

class POSifiedText(markovify.Text):
    '''
    Custom markovify.Text class
    Combines spacy POS tagging and newline sentence splitting.
    '''

    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

    def sentence_split(self, text):
        return re.split(r"\s*\n\s*", text)


class Modeller(object):
    '''Modeller class'''

    MAX_OVERLAP_RATIO = config.max_overlap_ratio
    MAX_OVERLAP_TOTAL = config.max_overlap_total
    DEFAULT_TRIES = config.default_tries

    def __init__(self, database):
        self.log = logging.getLogger(__name__)

        self.filter = None

        self.db = database
        self.get_model()


    def get_text(self, nick=None):
        '''Get list of messages from database
           messages are filtered by self.filter'''

        messages = []

        key = nick or self.filter

        if key:
            messages = [m.message for m in self.db.get(key)]
        else:
            messages = [m.message for m in self.db.get()]

        return messages

    def get_model(self, text=None, repeat=True):
        '''
        Creates a new model in a seperate thread
        Starts a timer to create a new model periodically
        '''

        self.log.debug("Getting model text...")

        # pulls values from db
        if not text:
            text = self.get_text()

        try:
            # generate model
            self.model = markovify.NewlineText("\n".join(text), state_size=3)

            self.log.debug("Generated model successfully.")
            self.log.debug("[MODEL ID]" + str(id(self.model)))

        except:
            self.log.debug("Model generation failed.")

        if repeat:
            self.log.debug("Spawning model timer...")

            # create thread to recreate model perodically.
            self.thread = threading.Timer(300, self.get_model)
            self.thread.start()
            self.log.debug("...Thread spawned.")


    def generate_message(self, message, **kwargs):
        '''Generate a message from model'''

        self.log.debug("generating message")
        message = self.model.make_sentence()

        return message
