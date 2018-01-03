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

from . import flashmquiz


def load(filename, name):
    f = open(filename, 'rb')
    try:
        cards = pickle.load(f)
        return flashmquiz.Quiz(name, cards)
    except EOFError:  # file is empty
        return flashmquiz.Quiz(name)
    f.close()


def dump(quiz, filename):
    # @param quiz has the type of flashmquiz.Quiz
    f = open(filename, 'wb')
    pickle.dump(quiz.cards, f)  # write the quiz to a file
    f.close()
