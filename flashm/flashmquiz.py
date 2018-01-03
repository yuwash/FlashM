# flashmquiz.py the internal quiz implementation for FlashM 0.1.0
#
# This only works within flashm.py
# see README file for copyright information and version history

import os


class Quiz:
    def __init__(self, name, cards=[], file_name=None):
        self.name = name
        self.cards = cards
        if file_name:
            self.file_name = file_name
        else:
            self.file_name = name
        self.modified = False
        self.len = len(self.cards)

    def append(self, card):
        self.cards.append(card)
        self.len += 1
        self.modified = True

    def remove(self, card_index):
        del self.cards[int(card_index)]
        self.len -= 1
        self.modified = True

    def temp_save(self, iomodule):
        # this actually writes the quiz to a file (with iomodule)
        iomodule.dump(self, self.file_name + '.tmp')

    def update(self, new_file_name=None):
        if not new_file_name or new_file_name == self.file_name:
            os.remove(self.file_name)  # remove old file
            os.renames(self.file_name + '.tmp', self.file_name)
        else:
            os.renames(self.file_name + '.tmp', new_file_name)
            self.file_name = new_file_name  # update internal file name
        self.modified = False
