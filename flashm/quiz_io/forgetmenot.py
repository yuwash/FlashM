# quiz file handling class for FlashM 0.1.1
# Deck export format of ForgetMeNot (github.com/tema6120/ForgetMeNot)
#
# This only works within flashm.py
# see README file for copyright information and version history

from .base import QuizIO
from ..flashmquiz import Quiz


def iter_cards_from_export(file_):
    question = answer = None
    add_emptyline = False
    while True:
        line = file_.readline()
        if not line:
            if answer is not None:
                yield question[:-1], answer.rstrip("\n")
            return
        if line == "Q:\n":
            question = ""
        elif line == "A:\n":
            answer = ""
        elif answer is not None:
            if line == "\n":
                if not add_emptyline:
                    add_emptyline = True
                    continue
                add_emptyline = False
                yield question[:-1], answer[:-1]
                question = answer = None
                continue
            elif add_emptyline:
                answer += "\n"
                add_emptyline = False
            answer += line
        elif question is not None:
            question += line


def write_cards(file_, cards):
    for question, answer in cards:
        file_.write("Q:\n{}\nA:\n{}\n\n\n".format(question, answer))


class ForgetMeNotExportQuizIO(QuizIO):
    @staticmethod
    def load(filename, name):
        with open(filename, 'r') as f:
            try:
                cards = list(iter_cards_from_export(f))
                return Quiz(name, cards, filename)
            except EOFError:  # file is empty
                return Quiz(name, filename=filename)

    @staticmethod
    def dump(quiz, filename):
        with open(filename, 'w') as f:
            write_cards(f, quiz.cards)  # write the quiz to a file
