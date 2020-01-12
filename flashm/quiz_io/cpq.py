# quiz file handling class for FlashM 0.1.0
# cPickle quiz files of FlashE
#
# This only works within flashm.py
# see README file for copyright information and version history

try:
    # for Python 2
    import cPickle as pickle
except ImportError:
    import pickle

from ..flashmquiz import Quiz
from .base import QuizIO


class PickleQuizIO(QuizIO):
    @staticmethod
    def load(filename, name):
        with open(filename, 'rb') as f:
            try:
                cards = pickle.load(f)
                return Quiz(name, cards, filename)
            except EOFError:  # file is empty
                return Quiz(name, filename=filename)

    @staticmethod
    def dump(quiz, filename):
        with open(filename, 'wb') as f:
            pickle.dump(quiz.cards, f)  # write the quiz to a file
