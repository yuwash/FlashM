# flashmquiz.py the internal quiz implementation for FlashM 0.1.0
#
# This only works within flashm.py
# see README file for copyright information and version history

import os


class Quiz:
    def __init__(self, name, set=[], file_name=None):
        self.name = name
        self.set = set
        if file_name:
            self.file_name = file_name
        else:
            self.file_name = name
        self.modified = False
        self.len = len(self.set)

    def append(self, card):
        self.set.append(card)
        self.len += 1
        self.modified = True

    def remove(self, card_index):
        del self.set[int(card_index)]
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
