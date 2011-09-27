# quiz file handling class for FlashM 0.1.0
# cPickle quiz files of FlashE
#
# This only works within flashm.py
# see README file for copyright information and version history

import cPickle, flashmquiz

def load(filename, name):
    f = open(filename)
    try:
        set = cPickle.load(f)
        return flashmquiz.quiz(name, set)
    except EOFError: #file is empty
        return flashmquiz.quiz(name)
    f.close()
  
def dump(quiz, filename):
    #@param quiz has the type of flashmquiz.quiz
    f = open(filename, 'w')
    cPickle.dump(quiz.set, f) # write the quiz to a file
    f.close()
