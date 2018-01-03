# fulltermui.py full screen terminal interface of FlashM
#
# This only works within flashm.py
# see README file for copyright information and version history

from __future__ import unicode_literals

from tempfile import NamedTemporaryFile
import subprocess
from prompt_toolkit.shortcuts import dialogs
from .ui import Ui, ReadCancelError

EDITOR = 'vim'


class FullTerminalUi(Ui):
    def prompt(self, description='', choices=[], default=None):
        dialog_kwargs = {'title': description}
        choiceshint = ', '.join(choices)
        if default:
            text = 'default: ' + default
            if choices:
                text += '; ' + choiceshint
        else:
            text = choiceshint
        if text:
            dialog_kwargs['text'] = text
        return dialogs.input_dialog(**dialog_kwargs)

    def write(self, content):
        dialogs.message_dialog(text=content)

    def read(self, hint='', default=None):
        if hint:
            text = hint
        else:
            text = ''
        if default is not None:
            defaulthint = '(default: {})'.format(default)
            if hint:
                text += '; ' + defaulthint
            else:
                text = defaulthint
        reply = dialogs.input_dialog(text=text)
        if reply:
            return reply
        elif reply is None:
            raise ReadCancelError
        else:
            return default

    def read_multiline(self, hint=''):
        self.write(hint)
        with NamedTemporaryFile(mode='r') as replyfile:
            ret = subprocess.call([EDITOR, replyfile.name])
            reply = replyfile.read()
            if ret != 0:
                self.write('discarding input:\n' + reply)
                return False
            return reply

    def dialog(self, type, hint=None):
        if type == self.DIALOG_TYPE_OK:
            self.write(hint)
        elif type == self.DIALOG_TYPE_YES_NO:
            return dialogs.yes_no_dialog(text=hint)

    def choice(self, options, hint=None, show_options=True):
        if not show_options:
            NotImplementedError('options are always shown!')
        reply = dialogs.radiolist_dialog(text=hint, values=[(
            key,
            value[0] + (' ' + value[1] if len(value) > 1 else ''),
        ) for key, value in options.items()])
        return reply
