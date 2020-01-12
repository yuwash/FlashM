# flashm.py the main module of FlashM 0.1.0
# call this file with python (http://python.org)
#
# see README file for copyright information and version history

import asyncio
import random
from . import flashmquiz
from .playback import Deck, playback_into_deck, playback_from_deck

from .quiz_io.cpq import PickleQuizIO
# cliui.py for the command-line interface
# cpq.py for FlashM to handle cPickle quiz files of FlashE
# pau.py for Pau quiz files of Pauker (pauker.sourceforge.net)
# mne.py for zipped quiz files of Mnemosyne (mnemosyne.org)

NOTICE = """FlashM version 0.1.0
  Copyright (C) 2011-2017 Yushin Washio (yuwash at yandex dot com)
  inspired by:
    FlashE A Very simple flash card program
    Copyright (C) 2003  Robie Lutsey (robie at 1937.net)
    https://sourceforge.net/projects/flashe/
  FlashM is provided 'as is' without any warranty under the terms of the
  GNU General Public License Version 3.
  This is free software, and you are welcome
  to improve and redistribute it under certain conditions; see the
  LICENSE file for details and the README file for more information
  about usage, installation and the history of this application."""

STD_IOMODULE = PickleQuizIO  # to use when file name extension doesn't imply
#  any specific quiz format (like .pau.gz for Pauker lessons)


def guess_file_type(filename):
    filename_low = filename.lower()
    if(filename_low.endswith('.pau.gz')):
        from .quiz_io.pau import PaukerQuizIO
        return PaukerQuizIO
    elif(filename_low.endswith('.zip')):
        from .quiz_io.mne import MnemosyneQuizIO
        return MnemosyneQuizIO
    else:
        return STD_IOMODULE


def str_get_card(card_str):
    card_str.replace('\\=', '&&eq;')
    card = card_str.split('=', 2)
    if len(card) == 2:
        for i in (0, 1):
            card[i] = card[i].strip().replace('&&eq;', '=')
        return card


class ReadCancelError(RuntimeError):
    pass


class StopPlayback(RuntimeError):
    pass


class Ui:
    def prompt(description='', choices=[], default=None):
        raise NotImplementedError('please implement in a subclass!')

    def read(self, hint='', default=None):
        reply = self.prompt(hint, ['q! to cancel'], default=default)
        if default is not None and reply == '':
            return default
        elif reply.lower() == 'q!':
            raise ReadCancelError
        else:
            return reply

    def read_multiline(hint=''):
        raise NotImplementedError('please implement in a subclass!')

    def write(content):
        raise NotImplementedError('please implement in a subclass!')

    def dialog(hint=None):
        raise NotImplementedError('please implement in a subclass!')

    def learn(self, quiz, flags=()):
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

        remaining = list(range(len(quiz.cards)))
        if 'LIST_ORDER' or 'REV_ORDER' in flags:
            rx = 0  # stays 0 within remaining; same for REV_ORDER,
            #  because in this case, list is reversed (below)
            if 'REV_ORDER' in flags:
                remaining.reverse()
        while remaining:  # isn't empty
            if not ('LIST_ORDER' or 'REV_ORDER' in flags):
                rx = random.randint(0, len(remaining)-1)
            x = remaining[rx]
            card = quiz.cards[x]
            if 'FLIP_QA' in flags:
                card.reverse()
            a = self.prompt(card[0] + '? Answer', ['optional; q! to end'])
            self.write('The default answer: ' + card[1])
            if a == 'q!':
                break
            elif 'CHKCORRECT' in flags and(a == card[1]):
                self.write("Congratulations, that's right!")
                del remaining[rx]
            elif 'ASKRIGHT' not in flags or self.prompt(
                'Was it right?', ['y/n']
            ).upper() == 'Y':
                del remaining[rx]

    def playback_show_card(self, card, duration):
        raise NotImplementedError('please implement in a subclass!')

    async def playback_async(self, quiz):
        deck = Deck()
        try:
            for i in playback_into_deck(deck, list(range(len(quiz.cards)))):
                await self.playback_show_card(quiz.cards[i], duration=2)
            for i in playback_from_deck(deck):
                await self.playback_show_card(quiz.cards[i], duration=2)
        except StopPlayback:
            return

    def playback(self, quiz):
        try:
            asyncio.get_event_loop().run_until_complete(
                self.playback_async(quiz))
        except KeyboardInterrupt:
            return

    @staticmethod
    def _card_repr(card, index=None):
        output = ''
        if index is not None:
            output += '[{:d}] '.format(index)
        return output + '[{}: {}]'.format(card[0], card[1])

    def show_card(self, card, index=None):
        self.write(self._card_repr(card, index=index))

    def show_cards(self, quiz, show_indices=False):
        if show_indices:
            for i, card in enumerate(quiz.cards):
                self.show_card(card, index=i)
        else:
            for card in quiz.cards:
                self.show_card(card)

    def delete_menu(self, quiz):
        if quiz.cards:  # isn't empty
            # list cards with indices
            self.show_cards(quiz, True)
            cardindices = self.prompt('Delete which card(s)?').split(',')
            deleted = []  # adapt to the modified indices
            # and avoid deleting the same index several times
            for istr in cardindices:
                try:
                    i = int(istr)
                    if i not in deleted:
                        # index has been changed after deletion
                        # of cards indexed below i
                        delta_i = sum(map(
                            lambda i: 1,
                            filter(lambda di: di < i, deleted),
                        ))
                        quiz.remove(i - delta_i)
                        deleted.append(i)  # contains original indices
                except IndexError:
                    self.write('IndexError: list index %s out of range' % istr)
                except ValueError:  # if istr doesn't contain a number
                    pass
        else:
            self.write('Set is empty!')

    def save(self, quiz, save_as=True, ask_whether_to_save=False):
        quiz.temp_save(STD_IOMODULE)
        if not ask_whether_to_save or self.yes_no_dialog(
            'Do you want to save changes?'
        ):
            if save_as:
                try:
                    new_file_name = self.read('Save as', quiz.file_name)
                    quiz.temp_save(guess_file_type(new_file_name))
                    # caution, temp_save only changes file type but preserves
                    # the old .tmp file name until update is called below
                    quiz.update(new_file_name)
                except ReadCancelError:
                    pass
            else:
                quiz.update()

    def getcard(self):
        try:
            question = self.read('What is the question?')
            answer = self.read('What is the answer?')
            return [question, answer]
        except ReadCancelError:
            return

    def text_import_menu(self, quiz):
        newitems = []
        userinput = self.read_multiline('Type in your text')
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
    EVT_PLAYBACK = 108
    EVT_QUIT = 105
    EVT_REV_LEARN = 106
    EVT_SHOW = 107
    options = {
        EVT_DELETE: ('d', 'Delete card(s)'),
        EVT_TEXT_IMPORT: ('i', 'Import cards from text'),
        EVT_LEARN: ('l', 'Learn'),
        EVT_NEW_CARD: ('n', 'Add new card'),
        EVT_PLAYBACK: ('p', 'Playback'),
        EVT_QUIT: ('q', 'Quit'),
        EVT_REV_LEARN: ('r', 'Learn with flipped cards'),
        EVT_SHOW: ('s', 'Show cards')
    }

    def __init__(self, cwq, uimodule, quiet=False):
        self.cwq = cwq  # working quiz (currently the only quiz)
        self.uimodule = uimodule
        self.quiet = quiet

    @staticmethod
    def open_quiz_file(uimodule, create=True, quiet=False):
        # @param create: whether to create if file doesn't exist yet

        result = False
        while result is False:
            try:
                name = uimodule.read('What is the quiz called?')
                if name == '':
                    uimodule.write('Error: Please enter a quiz name.')
                    continue
                try:
                    result = guess_file_type(name).load(name, name)
                    # filename=name
                except IOError:
                    if(create and uimodule.yes_no_dialog(
                        'The quiz file "' + name + '" doesn\'t exist. '
                        + 'Do you want to create it?'
                    )):
                        open(name, 'w').close()  # create an empty file
                        result = flashmquiz.Quiz(name)
            except ReadCancelError:  # user wants to quit during read
                return result
        return Session(result, uimodule, quiet)

    def start(self):
        if not self.quiet:
            self.uimodule.write(NOTICE)
        stay = self.cwq is not False
        cls = self
        while stay:
            command = self.uimodule.choice(
                cls.options, 'What do you want?', False)
            if command == cls.EVT_DELETE:
                self.uimodule.delete_menu(self.cwq)
            elif command == cls.EVT_TEXT_IMPORT:
                self.uimodule.text_import_menu(self.cwq)
                self.uimodule.save(self.cwq, True, True)
            elif command == cls.EVT_LEARN:
                self.uimodule.learn(self.cwq, ('CHKCORRECT', 'ASKRIGHT'))
            elif command == cls.EVT_NEW_CARD:
                newcard = self.uimodule.getcard()
                if newcard is not None:
                    self.cwq.append(newcard)
                    self.uimodule.save(self.cwq, True, True)
            elif command == cls.EVT_PLAYBACK:
                self.uimodule.playback(self.cwq)
            elif command == cls.EVT_QUIT:  # quit application
                stay = False
                if self.cwq.modified:  # if not saved after modification
                    self.uimodule.save(self.cwq, True, True)
            elif command == cls.EVT_REV_LEARN:
                self.uimodule.learn(
                    self.cwq,
                    ('FLIP_QA', 'CHKCORRECT', 'ASKRIGHT'),
                )
            elif command == cls.EVT_SHOW:
                self.uimodule.show_cards(self.cwq)
