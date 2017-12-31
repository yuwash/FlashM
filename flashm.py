#! /usr/bin/env python

# flashm.py the main module of FlashM 0.1.0
# call this file with python (http://python.org)
#
# see README file for copyright information and version history

import random
from argparse import ArgumentParser
import flashmquiz

import cliui
import cpq
import pau
import mne
# cliui.py for the command-line interface
# cpq.py for FlashM to handle cPickle quiz files of FlashE
# pau.py for Pau quiz files of Pauker (pauker.sourceforge.net)
# mne.py for zipped quiz files of Mnemosyne (mnemosyne.org)

NOTICE = """FlashM version 0.1.0
  Copyright (C) 2011 Yushin Washio (yuwas at ht.cx)
  inspired by:
    FlashE A Very simple flash card program
    Copyright (C) 2003  Robie Lutsey (robie at 1937.net)
    http://sourceforge.net/project/flashe
  FlashM is provided 'as is' without any warranty under the terms of the
  GNU General Public License Version 3.
  This is free software, and you are welcome
  to improve and redistribute it under certain conditions; see the
  LICENSE file for details and the README file for more information
  about usage, installation and the history of this application."""

UIMODULE = cliui
STD_IOMODULE = cpq  # what to use when file name extension doesn't imply
#  any specific quiz format (like .pau.gz for Pauker lessons)


def learn(quiz, flags=()):
    # @param flags: These are understood:
    # 'FLIP_QA': show answer and think about the question
    # 'LIST_ORDER': ask for questions in the listed order (default:
    #   random order)
    # 'REV_ORDER': ask for questions in the reversed listed order
    # 'CHKCORRECT': the program automatically recognizes your correct
    #   answer
    # 'ASKRIGHT': ask whether your answer was correct (to tolerate
    #   irrelevant differences and unpredicted alternative answers)
    #   (ignored if CHKCORRECT is not present)

    remaining = quiz.set
    if 'LIST_ORDER' or 'REV_ORDER' in flags:
        x = -1  # preset to get 0 as the first index; same for REV_ORDER,
        #  because in this case, list is reversed (below)
        if 'REV_ORDER' in flags:
            remaining.reverse()
    while remaining:  # isn't empty
        if 'LIST_ORDER' in flags:
            x += 1
        else:
            x = random.randint(0, len(remaining)-1)
        card = remaining[x]
        if 'FLIP_QA' in flags:
            card.reverse()
        a = UIMODULE.prompt(card[0] + '? Answer', ['optional; q! to end'])
        UIMODULE.write('The default answer: ' + card[1])
        if a == 'q!':
            remaining = []
        elif 'CHKCORRECT' in flags and(a == card[1]):
            UIMODULE.write("Congratulations, that's right!")
            del remaining[x]
        elif 'ASKRIGHT' not in flags or UIMODULE.prompt(
            'Was it right?', ['y/n']
        ).upper() == 'Y':
            del remaining[x]


def show_cards(quiz, show_indices=False):
    i = 0
    for card in quiz.set:
        output = ''
        if show_indices:
            output += '[%d] ' % i
            i += 1
        UIMODULE.write(output + '[' + card[0] + ': ' + card[1] + ']')


def delete_menu(quiz):
    if quiz.set:  # isn't empty
        # list cards with indices
        show_cards(True)
        cardindices = UIMODULE.prompt('Delete which card(s)?').split(',')
        deleted = []  # adapt to the modified indices
        # and avoid deleting the same index several times
        for istr in cardindices:
            try:
                i = int(istr)
                if i not in deleted:
                    for di in deleted:
                        if di < i:
                            i -= 1  # index has been changed after deletion
                            # of cards indexed below i
                    quiz.remove(i)
                    deleted.append(i)
            except IndexError:
                UIMODULE.write('IndexError: list index %s out of range' % istr)
            except ValueError:  # if istr doesn't contain a number
                pass
    else:
        UIMODULE.write('Set is empty!')


def guess_file_type(filename):
    if(filename[-7:].lower() == '.pau.gz'):
        return pau
    elif(filename[-4:].lower() == '.zip'):
        return mne
    else:
        return STD_IOMODULE


def save(quiz, save_as=True, ask_whether_to_save=False):
    quiz.temp_save(STD_IOMODULE)
    if not ask_whether_to_save or UIMODULE.dialog(
        UIMODULE.DIALOG_TYPE_YES_NO, 'Do you want to save changes?'
    ):
        if save_as:
            new_file_name = UIMODULE.read('Save as', quiz.file_name)
            if new_file_name:  # not canceled
                quiz.temp_save(guess_file_type(new_file_name))
                # caution, temp_save only changes file type but preserves
                # the old .tmp file name until update is called below
                quiz.update(new_file_name)
        else:
            quiz.update()


def getcard():
    question = UIMODULE.read('What is the question?')
    answer = UIMODULE.read('What is the answer?')
    if question and answer:  # aren't interrupted
        return [question, answer]


def str_get_card(card_str):
    card_str.replace('\=', '&&eq;')
    card = card_str.split('=', 2)
    if len(card) == 2:
        for i in (0, 1):
            card[i] = card[i].strip().replace('&&eq;', '=')
        return card


def text_import_menu(quiz):
    newitems = []
    userinput = UIMODULE.read_multiline('Type in your text')
    for line in userinput.split('\n'):
        newitems.append(str_get_card(line))
        if newitems[-1]:  # isn't None
            quiz.append(newitems[-1])
        else:
            del newitems[-1]
    return newitems


class Session:
    EVT_DELETE = 101
    EVT_TEXT_IMPORT = 102
    EVT_LEARN = 103
    EVT_NEW_CARD = 104
    EVT_QUIT = 105
    EVT_REV_LEARN = 106
    EVT_SHOW = 107
    options = {
        EVT_DELETE: ('d', 'Delete card(s)'),
        EVT_TEXT_IMPORT: ('i', 'Import cards from text'),
        EVT_LEARN: ('l', 'Learn'),
        EVT_NEW_CARD: ('n', 'Add new card'),
        EVT_QUIT: ('q', 'Quit'),
        EVT_REV_LEARN: ('r', 'Learn with flipped cards'),
        EVT_SHOW: ('s', 'Show cards')
    }

    def __init__(self, cwq, uimodule=UIMODULE, quiet=False):
        self.cwq = cwq  # working quiz (currently the only quiz)
        self.uimodule = uimodule
        self.quiet = quiet

    @classmethod
    def open_quiz_file(create=True, uimodule=UIMODULE, quiet=False):
        # @param create: whether to create if file doesn't exist yet

        result = False
        while result is False:
            name = uimodule.read('What is the quiz called?')
            if name == '':
                uimodule.write('Error: Please enter a quiz name.')
            elif name:  # is not None
                try:
                    result = guess_file_type(name).load(name, name)
                    # filename=name
                except IOError:
                    if(create and uimodule.dialog(
                        uimodule.DIALOG_TYPE_YES_NO,
                        'The quiz file "' + name + '" doesn\'t exist. '
                        + 'Do you want to create it?'
                    )):
                        open(name, 'w').close()  # create an empty file
                        result = flashmquiz.quiz(name)
            else:  # user wants to quit
                break
        return Session(result, uimodule, quiet)

    def start(self):
        if not self.quiet:
            self.uimodule.write(NOTICE)
        stay = self.cwq is not False
        # open_quiz_file returns False if user wants
        # to quit without opening or creating any quiz ('q!')
        cls = self
        while stay:
            command = self.uimodule.choice(
                cls.options, 'What do you want?', False)
            if command == cls.EVT_DELETE:
                delete_menu(self.cwq)
            elif command == cls.EVT_TEXT_IMPORT:
                text_import_menu(self.cwq)
                save(self.cwq, True, True)
            elif command == cls.EVT_LEARN:
                learn(self.cwq, ('CHKCORRECT', 'ASKRIGHT'))
            elif command == cls.EVT_NEW_CARD:
                newcard = getcard()
                self.cwq.append(newcard)
                save(self.cwq, True, True)
            elif command == cls.EVT_QUIT:  # quit application
                stay = False
                if self.cwq.modified:  # if not saved after modification
                    save(self.cwq, True, True)
            elif command == cls.EVT_REV_LEARN:
                learn(self.cwq, ('FLIP_QA', 'CHKCORRECT', 'ASKRIGHT'))
            elif command == cls.EVT_SHOW:
                show_cards(self.cwq)


def main():
    argparser = ArgumentParser(description=NOTICE)
    argparser.add_argument(
        '-q', '--quiet', action='store_true',
        help='turn off verbose output',
    )
    args = argparser.parse_args()
    Session.open_quiz_file(quiet=args.quiet).start()


if __name__ == "__main__":
    main()
